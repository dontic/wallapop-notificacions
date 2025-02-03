import requests
from celery import shared_task
from django.conf import settings
from datetime import datetime
from .models import WallapopSearch
import logging

log = logging.getLogger("app_logger")


@shared_task
def check_wallapop_search(search_id):
    log.info(f"Checking Wallapop search with ID {search_id}")

    search = WallapopSearch.objects.get(id=search_id)

    # Prepare API request
    params = {
        "keywords": search.keywords,
        "latitude": str(settings.WALLAPOP_LATITUDE).strip(),
        "longitude": str(settings.WALLAPOP_LONGITUDE).strip(),
        "order_by": "newest",
        "source": "search_box",
    }
    log.debug(f"Requesting Wallapop API with params: {params}")

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "es,en-US;q=0.9,en;q=0.8,es-ES;q=0.7",
        "Connection": "keep-alive",
        "DeviceOS": "0",
        "Host": "api.wallapop.com",
        "MPID": "-6463834448707591410",
        "Origin": "https://es.wallapop.com",
        "Referer": "https://es.wallapop.com/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        "X-AppVersion": "83990",
        "X-DeviceID": "37830b56-cecd-4d0d-aefe-29ab352149f0",
        "X-DeviceOS": "0",
        "sec-ch-ua": '"Not A(Brand";v="8", "Chromium";v="132", "Microsoft Edge";v="132"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
    }

    response = requests.get(
        "https://api.wallapop.com/api/v3/search", params=params, headers=headers
    )
    if not response.ok:
        log.error(f"Error fetching results: {response.status_code}")
        log.error(response.text)
        return f"Error fetching results: {response.status_code}"

    data = response.json()
    log.debug(f"Received data: {data}")
    items = data["data"]["section"]["payload"]["items"]

    # Get new items
    new_items = []
    last_id = search.last_id

    for item in items:
        if last_id and item["id"] == last_id:
            break
        new_items.append(
            {
                "title": item["title"],
                "price": f"{item['price']['amount']} {item['price']['currency']}",
                "url": f"https://es.wallapop.com/item/{item['web_slug']}",
                "location": f"{item['location']['city']}, {item['location']['region']}",
            }
        )

    log.debug(f"New items: {new_items}")

    if items:
        # Update last_id with the newest item's ID
        search.last_id = items[0]["id"]
        search.save()

    if new_items:
        log.info("Sending notification via NTFY")
        # Send notification via NTFY
        notification_text = "New items found:\n\n" + "\n\n".join(
            f"🏷️ {item['title']}\n💰 {item['price']}\n📍 {item['location']}\n🔗 {item['url']}"
            for item in new_items
        )

        requests.post(
            f"{settings.NTFY_URL}/{settings.NTFY_TOPIC}",
            data=notification_text.encode(encoding="utf-8"),
            headers={
                "Title": f"New items for '{search.keywords}'",
                "Priority": "default",
                "Tags": "shopping,new",
                "Authorization": f"Bearer {settings.NTFY_TOKEN}",
            },
        )

    return f"Processed {len(new_items)} new items"
