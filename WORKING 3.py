from bs4 import BeautifulSoup
import requests
import os

# CREATE FOLDER
def folder_create(images, folder_name):
    try:
        # folder creation
        os.mkdir(folder_name)

    # if folder exists with that name, ask another name
    except FileExistsError:
        print("Folder Exist with that name!")
        folder_create(images, input("Enter Folder Name:- "))

    # image downloading start
    download_images(images, folder_name)


# DOWNLOAD ALL IMAGES FROM THAT URL
def download_images(images, folder_name):
    # initial count is zero
    count = 0

    # print total images found in URL
    print(f"Total {len(images)} Image Found!")

    # checking if images is not zero
    if len(images) != 0:
        for i, image in enumerate(images):
            # From image tag, fetch image Source URL
            try:
                # In image tag, searching for "data-srcset"
                image_link = image["data-srcset"]
            except:
                try:
                    # In image tag, searching for "data-src"
                    image_link = image["data-src"]
                except:
                    try:
                        # In image tag, searching for "data-fallback-src"
                        image_link = image["data-fallback-src"]
                    except:
                        try:
                            # In image tag, searching for "src"
                            image_link = image["src"]
                        except:
                            pass

            # After getting Image Source URL
            # We will try to get the content of image
            try:
                r = requests.get(image_link).content
                try:
                    # possibility of decode
                    r = str(r, 'utf-8')
                except UnicodeDecodeError:
                    # After checking above condition, Image Download start
                    with open(f"{folder_name}/images{i + 1}.jpg", "wb+") as f:
                        f.write(r)

                    # counting number of image downloaded
                    count += 1
            except:
                pass

            # Break the loop if 10 images are downloaded
            if count == 10:
                break

        # There might be possible, that all
        # images not download
        # if all images download
        if count == len(images):
            print("All Images Downloaded!")

        # if all images not download
        else:
            print(f"Total {count} Images Downloaded Out of {min(10, len(images))}")


# MAIN FUNCTION START
def main(urls):
    for i, url in enumerate(urls, start=1):
        print(f"\nProcessing URL {i}: {url}")
        # content of URL
        r = requests.get(url)

        # Parse HTML Code
        soup = BeautifulSoup(r.text, 'html.parser')

        # find all images in URL
        images = soup.findAll('img')

        # Call folder create function
        folder_create(images, input("Enter Folder Name for URL {}: ".format(i)))


# take three URLs
urls = [input("Enter URL {}:- ".format(i + 1)) for i in range(3)]

# CALL MAIN FUNCTION
main(urls)
