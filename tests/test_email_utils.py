import pytest
from email_utils import process_query_and_response
from process_response import process_markdown


@pytest.fixture
def sample_query_and_response():
    query = "What is anemia? Please send the response to john@example.com"
    response = process_markdown(
        """
    ## Anemia

    Anemia is a condition in which you lack enough healthy red blood cells to carry adequate oxygen to your body's tissues. 
    
    Symptoms include:
    - Fatigue
    - Weakness
    - Pale or yellowish skin
    - Irregular heartbeats
    - Shortness of breath
    - Dizziness or lightheadedness
    - Chest pain
    - Cold hands and feet
    - Headaches

    For more information, visit:
    - American Society of Hematology. (2020). Anemia. [https://www.hematology.org/Patients/Anemia.aspx](https://www.hematology.org/Patients/Anemia.aspx)
    - National Institute of Diabetes and Digestive and Kidney Diseases. (2020). Anemia. [https://www.niddk.nih.gov/health-information/anemia](https://www.niddk.nih.gov/health-information/anemia)
    """
    )
    return query, response


def test_email_functionality(sample_query_and_response):
    query, response = sample_query_and_response
    process_query_and_response(query, response)
