from functions import yt_links

def main():
    url = "https://www.youtube.com/results?search_query="

    # label_dict = {'Technology': ['smartphone', 'pc hardware', 'computer gpu', 'laptop review'],
    #             'Educational-programming': ['python tutorials', 'c++ tutorials', 'c tutorials'],
    #             'Educational': ['math', 'statistics'],
    #             'Gaming': ['pc games review'],
    #             }
    label_dict = {'Technology': ['laptop review'],
            'Educational-programming': ['python tutorials', 'c++ tutorials', 'c tutorials'],
            'Educational': ['math', 'statistics'],
            'Gaming': ['pc games review'],
            }

    for key in label_dict:
        for val in label_dict[key]:
            yt_links(key=key, value=val, base_url=url)


if __name__ == "__main__":
    main()
        
        


