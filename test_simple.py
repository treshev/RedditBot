import requests

# string = 'https://i.imgur.com/lTEsySp.gif'
# url = string.replace(".gifv", ".mp4")
# print(url)

my_list = [
    'https://gfycat.com/FormalSilkyBunny',
    'https://imgur.com/Xnn0VRu',
    'https://imgur.com/lKh6tyK',
    'https://gfycat.com/OilyGlassDuck',
    'https://gfycat.com/EducatedLawfulElver',
    'https://gfycat.com/ThirstyDescriptiveGalapagossealion',
    'https://imgur.com/a/4Tibixb',
    'https://gfycat.com/UncomfortableAmazingGiraffe',
    'https://imgur.com/test.com',
    "https://thumbs.gfycat.com/FrighteningFrailDavidstiger"]


def get_gif_url_from_item_url(url: str):
    url = url.replace(".gifv", ".mp4")
    if url.endswith(".gif") or url.endswith(".mp4"):
        return url
    elif "gfycat.com" in url:
        src_name = url.split("gfycat.com/")[-1]
        response = requests.get("http://gfycat.com/cajax/get/{}".format(src_name))
        # print(response.json())
        gif_json = response.json().get("gfyItem")
        gif_url = None
        if gif_json:
            gif_url = gif_json.get('max5mbGif', response.json()["gfyItem"]["gifUrl"])
        return gif_url
    elif "imgur.com" in url and url.split("/")[-1].count('.') == 0:
        return url + ".mp4"


if __name__ == '__main__':
    for item in my_list:
        res = get_gif_url_from_item_url(item)
        print("Src:{:60s} result {}".format(item, res))
    # r = get_gif_url_from_item_url("https://thumbs.gfycat.com/FrighteningFrailDavidstiger")
    # print(r)
