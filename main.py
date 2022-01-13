from google.cloud import vision
from google.protobuf import field_mask_pb2 as field_mask
from google.cloud import storage
import urllib.request
from csv import reader


def create_bucket(bucket_name):
    """
    Create a new bucket in the US region with the coldline storage
    class
    """
    storage_client = storage.Client()

    bucket = storage_client.bucket(bucket_name)
    bucket.storage_class = "COLDLINE"
    new_bucket = storage_client.create_bucket(bucket, location="us")

    print(
        "Created bucket {} in {} with storage class {}".format(
            new_bucket.name, new_bucket.location, new_bucket.storage_class
        )
    )
    return new_bucket


def upload_image(bucket_name, img_url):
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob_name = img_url.split('//')[1]
    blob = bucket.blob(blob_name)

    # try to read the image URL
    try:
        with urllib.request.urlopen(img_url) as response:
            # check if URL contains an image
            info = response.info()
            if (info.get_content_type().startswith("image")):
                blob.upload_from_string(response.read(), content_type=info.get_content_type())
                return 'gs://' + bucket_name + '/' + blob_name
            else:
                return None
    except Exception as e:
        print(e)
        return None


def create_product_set(
        project_id, location, product_set_id, product_set_display_name):
    """Create a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_set_id: Id of the product set.
        product_set_display_name: Display name of the product set.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # Create a product set with the product set specification in the region.
    product_set = vision.ProductSet(
        display_name=product_set_display_name)

    # The response is the product set with `name` populated.
    response = client.create_product_set(
        parent=location_path,
        product_set=product_set,
        product_set_id=product_set_id)

    # Display the product set information.
    print('Product set name: {}'.format(response.name))


def create_product(
        project_id, location, product_id, product_display_name, product_description,
        product_category, product_labels):
    """Create one product.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_display_name: Display name of the product.
        product_category: Category of the product.
    """
    client = vision.ProductSearchClient()

    # A resource that represents Google Cloud Platform location.
    location_path = f"projects/{project_id}/locations/{location}"

    # Create a product with the product specification in the region.
    # Set product display name and product category.
    product = vision.Product(
        display_name=product_display_name,
        description=product_description,
        product_category=product_category,
        product_labels=product_labels)

    # The response is the product with the `name` field populated.
    response = client.create_product(
        parent=location_path,
        product=product,
        product_id=product_id)

    # Display the product information.
    print('Product name: {}'.format(response.name))


def add_product_to_product_set(
        project_id, location, product_id, product_set_id):
    """Add a product to a product set.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        product_set_id: Id of the product set.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product set.
    product_set_path = client.product_set_path(
        project=project_id, location=location,
        product_set=product_set_id)

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Add the product to the product set.
    client.add_product_to_product_set(
        name=product_set_path, product=product_path)
    print('Product added to product set.')


def create_reference_image(
        project_id, location, product_id, reference_image_id, gcs_uri):
    """Create a reference image.
    Args:
        project_id: Id of the project.
        location: A compute region name.
        product_id: Id of the product.
        reference_image_id: Id of the reference image.
        gcs_uri: Google Cloud Storage path of the input image.
    """
    client = vision.ProductSearchClient()

    # Get the full path of the product.
    product_path = client.product_path(
        project=project_id, location=location, product=product_id)

    # Create a reference image.
    reference_image = vision.ReferenceImage(uri=gcs_uri)

    # The response is the reference image with `name` populated.
    image = client.create_reference_image(
        parent=product_path,
        reference_image=reference_image,
        reference_image_id=reference_image_id)

    # Display the reference image information.
    print('Reference image name: {}'.format(image.name))
    print('Reference image uri: {}'.format(image.uri))


if __name__ == '__main__':
    bucket_name = "beni-ai-engine"
    project_id = "beni-ai-engine"
    location = "us-east1"
    product_set_id = 'BENI_CLOTH'
    try:
        create_bucket(bucket_name)
    except Exception as e:
        print(e)
    try:
        create_product_set(project_id, location, product_set_id, "TEST_CLOTH")
    except Exception as e:
        print(e)
    with open('product_catalog_productbase.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        header = next(csv_reader)
        if header is not None:
            for row in csv_reader:
                beni_product_id = row[1]
                product_id = row[2]
                img_url = row[4]
                brand = row[7]
                product_title = row[8]
                product_description = row[9]
                gender = row[11]
                color = row[12]
                product_category = row[20]
                product_labels = [
                    vision.Product.KeyValue(key='brand', value=brand),
                    vision.Product.KeyValue(key='gender', value=gender),
                    vision.Product.KeyValue(key='color', value=color),
                    vision.Product.KeyValue(key='category', value=product_category)
                ]
                try:
                    create_product(project_id, location, beni_product_id, product_title, product_description, 'apparel',
                                   product_labels)
                except Exception as e:
                    print(e)
                try:
                    add_product_to_product_set(project_id, location, beni_product_id, product_set_id)
                except Exception as e:
                    print(e)
                try:
                    gcs_uri = upload_image(bucket_name, img_url)
                    if gcs_uri is not None:
                        create_reference_image(project_id, location, beni_product_id, product_id, gcs_uri)
                except Exception as e:
                    print(e)
