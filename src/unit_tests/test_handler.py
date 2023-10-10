from handler import get_s3_image, image_to_thumbnail, upload_to_s3
from PIL import Image
from botocore.stub import ANY


def test_get_file(s3_stub):
    test_image = open('src/unit_tests/data/cover1.jpg', 'rb')
    s3_stub.add_response(
        "get_object",
        expected_params={"Bucket": "example-bucket", "Key": "foobar"},
        service_response={
            'Body': test_image,
        },
    )

    result = get_s3_image(bucket="example-bucket", key="foobar")
    assert result.format == 'JPEG'


def test_image_to_thumbnail():
    test_image = Image.open('src/unit_tests/data/cover1.jpg')
    result = image_to_thumbnail(test_image)
    assert result.size == (128, 128)


def test_upload_to_s3(s3_stub):
    test_image = Image.open('src/unit_tests/data/cover1_thumbnail.png')
    s3_stub.add_response(
        "put_object",
        expected_params={
            "Bucket": "bucket-pytest-test",
            "Key": "foobar",
            "Body": ANY,
            "ContentType": "image/png"
        },
        service_response={},
    )

    result = upload_to_s3("foobar", test_image)
    assert result == "https://s3.amazonaws.com/bucket-pytest-test/foobar"
