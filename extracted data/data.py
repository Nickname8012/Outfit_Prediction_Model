from icrawler.builtin import GoogleImageCrawler
import os
import re

def sanitize(text):
    # Create a safe folder name from the query text.
    return re.sub(r'\W+', '_', text).strip('_')

def download_images(query, max_num, output_dir):
    subfolder = os.path.join(output_dir, sanitize(query))
    os.makedirs(subfolder, exist_ok=True)
    google_crawler = GoogleImageCrawler(storage={'root_dir': subfolder})
    google_crawler.crawl(keyword=query, max_num=max_num)

if __name__ == '__main__':
    # Original blazer queries (modify or add more if desired)
    blazer_queries = [
        "men wearing navy blue blazer",
        "men wearing charcoal grey blazer",
        "men wearing black blazer",
        "men wearing brown blazer",
        "men wearing burgundy blazer",
        "men wearing olive blazer",
        "men wearing light blue blazer",
        "men wearing dark green blazer",
        "men wearing pinstripe blazer",
        "men wearing checked blazer",
        "men wearing tweed blazer",
        "men wearing formal dark blazer",
        "men wearing pastel blazer",
        "men wearing multicolor patterned blazer",
        "men wearing red blazer",
        "men wearing white blazer",
        "men wearing beige blazer",
        "men wearing smart casual blazer",
        "men wearing slim fit blazer",
        "men wearing double button blazer",
        "men wearing modern cut blazer",
        "men wearing classic style blazer",
        "men wearing formal lapel blazer",
        "men wearing casual blazer with jeans",
        "men wearing blazer with vest",
        "men wearing dark burgundy blazer",
        "men wearing rich colored blazer",
        "men wearing colorful patterned blazer",
        "men wearing vintage blazer",
        "men wearing modern navy blazer",
        "men wearing elegant grey blazer",
        "men wearing sharp black blazer",
        "men wearing textured blazer",
        "men wearing sophisticated blazer",
        "men wearing minimalistic blazer",
        "men wearing ornate blazer",
        "men wearing refined blazer",
        "men wearing blended color blazer",
        "men wearing light natural toned blazer",
        "men wearing single button blazer",
        "men wearing double-breasted blazer",
        "men wearing smart business blazer",
        "men wearing relaxed fit blazer",
        "men wearing sporty blazer",
        "men wearing fashion-forward blazer",
        "men wearing bespoke tailored blazer",
        "men wearing contrasting blazer"
    ]
    
    # Define tie colors and shoe shades
    tie_colors = [
        "red tie",
        "blue tie",
        "green tie",
        "yellow tie",
        "purple tie"
    ]
    
    shoe_shades = [
        "black shoes",
        "brown shoes",
        "white shoes",
        "grey shoes",
        "beige shoes"
    ]
    
    # Build combined queries that add tie and shoe combinations.
    combined_queries = []
    for blazer in blazer_queries:
        # Base query with blazer and tie (if the style was meant for tie, you may add "with tie")
        base_query = f"{blazer} with tie"
        combined_queries.append(base_query)
        
        # Add a variant with just a specific tie color.
        for tie in tie_colors:
            combined_queries.append(f"{blazer} with {tie}")
        
        # Add a variant with just a specific shoe shade.
        for shoe in shoe_shades:
            combined_queries.append(f"{blazer} with {shoe}")
        
        # Add a variant with both a specific tie color and shoe shade.
        for tie in tie_colors:
            for shoe in shoe_shades:
                combined_queries.append(f"{blazer} with {tie} and {shoe}")
    
    output_directory = "./image_dataset"
    images_per_query = 5  # Adjust the number of images for each query as needed
    
    for query in combined_queries:
        print(f"Downloading images for query: {query}")
        download_images(query, images_per_query, output_directory)