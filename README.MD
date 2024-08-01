# Terraform Webscraping Tokopedia with Selenium

This project sets up a web scraping environment for Tokopedia using Terraform, Selenium, Docker, and Google Cloud Platform (GCP). Deploying multi vm on selenium will reduce the time scraping due to vm is having internet bandwith in every vm. So, using terraform/tofu is the best practices for deploying multi vm. Also, using docker container give you advantages to be easy installation with docker image or incase you want to deploy more container in vm.

## Prerequisites

- [Terraform](https://www.terraform.io/downloads.html) installed
- [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and configured
- [Docker](https://www.docker.com/get-started) installed
- [Chromedriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) compatible with your Chrome version
- [Selenium](https://www.selenium.dev/documentation/en/getting_started_with_webdriver/) installed

## Setup Instructions

1. **Clone the repository and navigate to the main deployment directory:**
    ```sh
    cd /main_deploy
    ```

2. **Initialize Terraform:**
    ```sh
    terraform init
    ```

3. **Create an execution plan:**
    ```sh
    terraform plan
    ```

4. **Apply the Terraform configuration:**
    ```sh
    terraform apply -auto-approve
    ```

5. **Destroy the Terraform-managed infrastructure when done:**
    ```sh
    terraform destroy
    ```

## Notes

- Occasionally, there may be issues with Chromedriver compatibility. Ensure that the Chromedriver version matches the required Selenium version.
- For more details on Chromedriver versions, refer to the [official Chromedriver documentation](https://sites.google.com/a/chromium.org/chromedriver/downloads).

## Additional Resources

- [Terraform Documentation](https://www.terraform.io/docs)
- [Google Cloud Platform Documentation](https://cloud.google.com/docs)
- [Docker Documentation](https://docs.docker.com/)
- [Selenium Documentation](https://www.selenium.dev/documentation/en/)

Thank you,
Azhar Izzannada Elbachtiar


