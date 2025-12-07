import os

def create_affiliate_funnel(title, link):
    html = f"""
    <html>
        <body>
            <h1>{title}</h1>
            <p>🔥 Exclusive Offer</p>
            <a href="{link}">Buy Now</a>
        </body>
    </html>
    """

    os.makedirs("funnels", exist_ok=True)
    path = f"funnels/{title}.html"

    with open(path, "w") as f:
        f.write(html)

    return {"status": "success", "path": path}
