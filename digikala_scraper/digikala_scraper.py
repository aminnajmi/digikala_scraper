import requests
import pandas as pd
import time


base_url = "https://api.digikala.com/v1/categories/mobile-phone/search/?page="
max_pages = 5
products = []


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Accept": "application/json"
}


for page in range(1, max_pages + 1):
    print(f"⏳ Fetching page {page}...")
    url = base_url + str(page)
    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        items = data.get('data', {}).get('products', [])
        if not items:
            print(f"⚠️ No products found on page {page}")
            continue

        for item in items:
            title = item.get('title_fa') or item.get('title_en') or 'No title'
            price = item.get('default_variant', {}).get('price', {}).get('selling_price') or 'N/A'
            rating = item.get('rating', {}).get('rate') or 'No rating'
            seller = item.get('default_variant', {}).get('seller', {}).get('title') or 'Unknown'

            products.append([title, price, rating, seller])

        time.sleep(1)

    except Exception as e:
        print(f"❌ Error on page {page}: {e}")
        continue


df = pd.DataFrame(products, columns=['Product Title', 'Price (IRR)', 'Rating', 'Seller'])


df.to_csv('digikala_products.csv', index=False, encoding='utf-8')


html_output = df.to_html(index=False, border=0, justify="center", classes="table table-striped")
with open('digikala_products.html', 'w', encoding='utf-8') as f:
    f.write("""
    <html>
    <head>
        <title>Digikala Products</title>
        <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
    </head>
    <body class="p-4">
        <h2 class="text-center mb-4">📦 Mobile Products from Digikala</h2>
        """ + html_output + """
    </body>
    </html>
    """)

print(f"\n✅ {len(products)} products saved to digikala_products.csv and digikala_products.html.")
