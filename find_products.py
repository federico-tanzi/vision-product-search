from google.cloud import vision


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

    index_time = response.product_search_results.index_time
    print('Product set index time: {}'.format(index_time))

    return response.product_search_results.results


def print_results(results, file_path):
    print('Search results for {}:'.format(file_path))
    for result in results:
        product = result.product

        print('Score(Confidence): {}'.format(result.score))
        print('Image name: {}'.format(result.image))

        print('Product name: {}'.format(product.name))
        print('Product display name: {}'.format(
            product.display_name))
        print('Product description: {}\n'.format(product.description))
        print('Product labels: {}\n'.format(product.product_labels))


if __name__ == '__main__':
    project_id = "beni-ai-engine"
    location = "us-east1"
    product_set_id = 'BENI_CLOTH'
    product_category = 'apparel'

    filter1 = None
    results1 = get_similar_products_file(project_id, location, product_set_id, product_category, 'test.jpeg',
                                        filter1, 10)
    print_results(results1, 'test.jpeg')

    filter2 = 'color = Black AND gender = Women'
    results2 = get_similar_products_file(project_id, location, product_set_id, product_category, 'test-2.jpeg',
                                         filter2, 10)
    print_results(results2, 'test-2.jpeg')
