import requests

def scrape_toko_api(shop_id, user_id):
    url = f"https://shopee.co.id/api/v4/seller_operation/get_rating_summary_new?replied=false&shop_id={shop_id}&userid={user_id}"
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # akan menimbulkan error jika status bukan 200

        data = response.json().get("data")
        if data:
            hasil = {
                "rating_total": data.get("rating_total"),
                "rating_star": data.get("rating_star"),
                "rating_count": data.get("rating_count")
            }
            return hasil
        else:
            return {"error": "Data tidak ditemukan di response."}

    except Exception as e:
        return {"error": str(e)}
