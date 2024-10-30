import requests
import pandas as pd
import time


# Constants
GITHUB_API_URL = "https://api.github.com"
CITY = "Hyderabad"
MIN_FOLLOWERS = 50
HEADERS = {"Authorization": "token removed_access_token_for_security_reason"}


# Helper function to clean up company names
def clean_company_name(company):
    if not company:
        return ""
    company = company.strip()
    if company.startswith("@"):
        company = company[1:]
    return company.upper()


# Fetch users with more than 50 followers in Hyderabad
def fetch_users_in_city(city, min_followers):
    users = []
    page = 1

    while True:
        url = f"{GITHUB_API_URL}/search/users?q=location:{city}+followers:>{min_followers}&page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        if "items" not in data:
            break

        users.extend(data["items"])

        # Exit if there are no more pages
        if len(data["items"]) < 100:
            break

        page += 1
        time.sleep(2)  # Avoid hitting the rate limit

    return users


# Fetch detailed user data
def fetch_user_details(user_login):
    url = f"{GITHUB_API_URL}/users/{user_login}"
    response = requests.get(url, headers=HEADERS)
    return response.json()


# Fetch repositories for a user
def fetch_user_repositories(user_login):
    repos = []
    page = 1

    while True:
        url = f"{GITHUB_API_URL}/users/{user_login}/repos?sort=pushed&page={page}&per_page=100"
        response = requests.get(url, headers=HEADERS)
        data = response.json()

        if len(data) == 0:
            break

        repos.extend(data)

        if len(data) < 100 or len(repos) >= 500:
            break

        page += 1
        time.sleep(1)  # Avoid hitting the rate limit

    return repos[:500]  # Limit to 500 most recent


# Main function to fetch data and store in CSV
def main():
    users = fetch_users_in_city(CITY, MIN_FOLLOWERS)

    user_data = []
    repo_data = []

    print("fetched user data")

    for user in users:
        user_details = fetch_user_details(user["login"])

        print("user")
        # Extract user data
        user_data.append(
            {
                "login": user["login"],
                "name": user_details.get("name", ""),
                "company": clean_company_name(user_details.get("company", "")),
                "location": user_details.get("location", ""),
                "email": user_details.get("email", ""),
                "hireable": user_details.get("hireable", ""),
                "bio": user_details.get("bio", ""),
                "public_repos": user_details.get("public_repos", 0),
                "followers": user_details.get("followers", 0),
                "following": user_details.get("following", 0),
                "created_at": user_details.get("created_at", ""),
            }
        )

        # Fetch repositories and extract repo data
        print("their repos")

        repos = fetch_user_repositories(user["login"])
        for repo in repos:
            repo_data.append(
                {
                    "login": user["login"],
                    "full_name": repo["full_name"],
                    "created_at": repo["created_at"],
                    "stargazers_count": repo["stargazers_count"],
                    "watchers_count": repo["watchers_count"],
                    "language": repo.get("language", ""),
                    "has_projects": repo["has_projects"],
                    "has_wiki": repo["has_wiki"],
                    "license_name": (
                        repo["license"]["name"] if repo["license"] else None
                    ),
                }
            )
        print("next")

    print("saving data")

    # Save to CSV files
    pd.DataFrame(user_data).to_csv("users.csv", index=False)
    pd.DataFrame(repo_data).to_csv("repositories.csv", index=False)

    print("PROCESS COMPLETE!")


# Run main function
if __name__ == "__main__":
    main()
