import requests
from bs4 import BeautifulSoup


def img_get(search_term):
    # Function to extract image URLs and stop after the fifth one is found
    def gets_url(page_content, classes, location, source):
        soup = BeautifulSoup(page_content, "html.parser")
        results = []
        for a in soup.findAll(attrs={"class": classes}):
            name = a.find(location)
            if name:
                results.append(name.get(source))
                if len(results) == 5:  # Stop after finding the fifth image URL
                    break
        return results

    # Format the URL with the user input
    url = f"https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={
        search_term}&_sacat=0&_odkw=laptop&_osacat=0"

    headers = {
        'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Ensure the request was successful

    # Extract image URLs
    image_urls = gets_url(
        response.content, "s-item__image-wrapper image-treatment", "img", "src")

    # Return the 5th image URL found
    if len(image_urls) == 5:
        return image_urls[4]
    else:
        return "Less than five images found."


# if __name__ == "__main__":
#    # Get user input for the search term
#    search_term = input("Enter the search term: ")
#    fifth_image_url = fetch_fifth_image_url(search_term)
#    print(fifth_image_url)
