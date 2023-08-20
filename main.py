from youtube import *


if __name__ == "__main__":
    youtube = yt_authenticate()

    query = input("\nEnter a search query: ")

    search_results = yt_search(youtube, query)
    video_ids = []
    print("\nSearch Results:")
    for idx, result in enumerate(search_results):
        video_ids.append(result["video_id"])
        print(
            f"{idx}: {result['title']}\n\thttps://www.youtube.com/watch?v={result['video_id']}"
        )

    print()

    playlist_title = input("Enter a title for this playlist: ")
    playlist_description = (
        f"Playlist created from the search results of the following query: {query}"
    )

    playlist_id = yt_create_playlist(youtube, playlist_title, playlist_description)

    yt_add_videos_to_playlist(youtube, playlist_id, video_ids)

    # description = yt_get_video_description(youtube, search_results[0]["video_id"])
    # print(f"\nVideo Description for {search_results[0]['title']}:\n\n{description}")
