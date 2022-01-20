from google.cloud import vision
from datetime import datetime


def get_similar_products_file(
        project_id,
        location,
        product_set_id,
        product_category,
        file_path,
        filter,
        max_results
):
    """Search similar products to image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_category: Category of the product.
        file_path: Local file path of the image to be searched.
        filter: Condition to be applied on the labels.
                Example for filter: (color = red OR color = blue) AND style = kids
                It will search on all products with the following labels:
                color:red AND style:kids
                color:blue AND style:kids
        max_results: The maximum number of results (matches) to return. If omitted, all results are returned.
    """
    # product_search_client is needed only for its helper methods.
    product_search_client = vision.ProductSearchClient()
    image_annotator_client = vision.ImageAnnotatorClient()

    # Read the image as a stream of bytes.
    with open(file_path, 'rb') as image_file:
        content = image_file.read()

    # Create annotate image request along with product search feature.
    image = vision.Image(content=content)

    # product search specific parameters
    product_set_path = product_search_client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)
    product_search_params = vision.ProductSearchParams(
        product_set=product_set_path,
        product_categories=[product_category],
        filter=filter)
    image_context = vision.ImageContext(
        product_search_params=product_search_params)

    # Search products similar to the image.
    response = image_annotator_client.product_search(
        image,
        image_context=image_context,
        max_results=max_results
    )

    return response.product_search_results


def print_results(product_search_results):
    index_time = product_search_results.index_time
    print('Product set index time: {}'.format(index_time))
    results = product_search_results.results
    print('Results len: {}'.format(len(results)))
    for result in results:
        print('Score(Confidence): {}'.format(result.score))
        print('Image name: {}'.format(result.image))

        product = result.product
        print('Product name: {}'.format(product.name))
        print('Product display name: {}'.format(product.display_name))
        print('Product description: {}'.format(product.description))
        print('Product labels: {}'.format(product.product_labels))


def case_1(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 1')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'hollister_black_shirt_1.jpg', None, None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}'.format('hollister_black_shirt_1.jpg'))
    print_results(result)


def case_1_b(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 1 B')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_black_shirt_2.jpg', None, None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}'.format('zara_black_shirt_2.jpg'))
    print_results(result)


def case_1_c(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 1 C')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_orange_shirt_2.jpg', None, None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}'.format('zara_orange_shirt_2.jpg'))
    print_results(result)


def case_2(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 2')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'hollister_black_shirt_1.jpg', 'color = black', None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}, filter: {}'.format('hollister_black_shirt_1.jpg', 'color = black'))
    print_results(result)


def case_2_b(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 2 B')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_black_shirt_2.jpg', 'color = black', None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}, filter: {}'.format('zara_black_shirt_2.jpg', 'color = black'))
    print_results(result)


def case_2_c(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 2 C')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_orange_shirt_2.jpg', 'color = orange', None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}, filter: {}'.format('zara_orange_shirt_2.jpg', 'color = orange'))
    print_results(result)


def case_3(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 3')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'hollister_black_shirt_1.jpg', 'color = white', None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}, filter: {}'.format('hollister_black_shirt_1.jpg', 'color = white'))
    print_results(result)


def case_3_b(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 3 B')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_black_shirt_2.jpg', 'color = white', None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}, filter: {}'.format('zara_black_shirt_2.jpg', 'color = white'))
    print_results(result)


def case_3_c(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 3 C')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_orange_shirt_2.jpg', 'color = white', None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}, filter: {}'.format('zara_orange_shirt_2.jpg', 'color = white'))
    print_results(result)


def case_4(project_id, location, product_set_id, product_category):
    print('---------------------Test Case 4')
    start_time = datetime.now()
    result = get_similar_products_file(project_id, location, product_set_id, product_category,
                                       'zara_black_shirt_1_worn.jpg', None, None)
    end_time = datetime.now()
    diff_time = end_time - start_time
    print('Process Time: {}'.format(diff_time))
    print('Search results for image: {}'.format('zara_black_shirt_1_worn.jpg'))
    print_results(result)


if __name__ == '__main__':
    project_id = "beni-ai-engine"
    location = "us-east1"
    product_set_id = 'BENI_TEST_CASES'
    product_category = 'apparel'

    case_1(project_id, location, product_set_id, product_category)
    case_1_b(project_id, location, product_set_id, product_category)
    case_1_c(project_id, location, product_set_id, product_category)
    case_2(project_id, location, product_set_id, product_category)
    case_2_b(project_id, location, product_set_id, product_category)
    case_2_c(project_id, location, product_set_id, product_category)
    case_3(project_id, location, product_set_id, product_category)
    case_3_b(project_id, location, product_set_id, product_category)
    case_3_c(project_id, location, product_set_id, product_category)
    case_4(project_id, location, product_set_id, product_category)
