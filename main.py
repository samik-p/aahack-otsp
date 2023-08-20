from youtube import *


if __name__ == "__main__":
    youtube = yt_authenticate()

    query = input("\nEnter a search query: ")

    search_results = yt_search(youtube, query)
    print("\nSearch Results:")
    # print(search_results)
    for idx, result in enumerate(search_results):
        print(
            f"{idx}: {result['title']}\n\thttps://www.youtube.com/watch?v={result['video_id']}"
        )

    description = yt_get_video_description(youtube, search_results[0]["video_id"])
    print(f"\nVideo Description for {search_results[0]['title']}:\n\n{description}")
