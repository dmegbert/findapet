from z_archive.scraping.dog_scraping import get_all_breed_links


def test_get_all_breed_links():
    all_breed_links = get_all_breed_links()
    assert len(all_breed_links) == 182
    assert 'https://www.petfinder.com/dog-breeds/affenpinscher/' in all_breed_links
    assert 'https://www.petfinder.com/dog-breeds/yorkshire-terrier/' in all_breed_links

