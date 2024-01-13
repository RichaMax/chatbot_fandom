from parser.valheim_page_scraper import ValheimPageScraper


def test_biome_page():
    test_url = "https://valheim.fandom.com/wiki/Meadows"
    page_scraper = ValheimPageScraper(page_url=test_url)
    page_content = page_scraper.scrape()
    # print(page_content)
    return page_scraper


def test_animal_page():
    test_url = "https://valheim.fandom.com/wiki/Deer"
    page_scraper = ValheimPageScraper(page_url=test_url)
    page_content = page_scraper.scrape()
    # print(page_content)
    return page_scraper


def test_skill_page():
    test_url = "https://valheim.fandom.com/wiki/Spears"
    page_scraper = ValheimPageScraper(page_url=test_url)
    page_content = page_scraper.scrape()
    # print(page_content)
    return page_scraper


def test_scrape_page(page_url):
    page_scraper = ValheimPageScraper(page_url=page_url)
    page_content = page_scraper.scrape()
    return page_scraper


if __name__ == "__main__":
    biome_test_page = "https://valheim.fandom.com/wiki/Meadows"
    biome_page = test_scrape_page(biome_test_page)
    print(">>>Biome page")
    print(">>>Extracted text")
    print(biome_page.page_content)
    print(f"metadata: {biome_page.metadata}")
    print("-----------")
    animal_test_page = "https://valheim.fandom.com/wiki/Deer"
    animal_page = test_scrape_page(animal_test_page)
    print(">>>Creature page")
    print(">>>Extracted text:")
    print(animal_page.page_content)
    print(f"metadata: {animal_page.metadata}")
    print("-----------")
    skill_test_page = "https://valheim.fandom.com/wiki/Spears"
    skill_page = test_scrape_page(skill_test_page)
    print(">>>Skill page")
    print(">>>Extracted text:")
    print(skill_page.page_content)
    print(f"metadata: {skill_page.metadata}")
    print("-----------")
    food_test_page = "https://valheim.fandom.com/wiki/Cooked_deer_meat"
    food_page = test_scrape_page(food_test_page)
    print(">>>Food page")
    print(">>>Extracted text:")
    print(food_page.page_content)
    print(f"metadata: {food_page.metadata}")
    print("-----------")
    generic_test_page = "https://valheim.fandom.com/wiki/Weapons"
    generic_page = test_scrape_page(generic_test_page)
    print(">>>Generic page")
    print(">>>Extracted text:")
    print(generic_page.page_content)
    print(f"metadata: {generic_page.metadata}")
    print("-----------")
    boss_test_page = "https://valheim.fandom.com/wiki/Yagluth"
    boss_page = test_scrape_page(boss_test_page)
    print(">>>Boss page")
    print(">>>Extracted text:")
    print(boss_page.page_content)
    print(f"metadata: {boss_page.metadata}")
    print("-----------")
    skill_test_page = "https://valheim.fandom.com/wiki/Skills"
    skill_page = test_scrape_page(skill_test_page)
    print(">>>Skills page")
    print(">>>Extracted text:")
    print(skill_page.page_content)
    print(f"metadata: {skill_page.metadata}")
    print("-----------")
