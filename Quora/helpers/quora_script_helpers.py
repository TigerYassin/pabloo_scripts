import shlex
import subprocess
import json
from time import sleep
import pandas as pd


class QuoraScriptHelpers:
    """
        Functions:
            1. save_users_to_file (saves all quora space followers to .xlsx file)
            2. Send follower request (Should I put all functions here or make a separate class?)
    """

    FILE_NAME_QUORA_USERS = "quora_users.xlsx"


    @staticmethod
    def save_users_to_file(quora_space_url: str) -> list:
        """ Scrapes all user ids for the given quora space. """
        # TODO: Change the url, and tribeId (Where do we get the tribeId from?)
        print("This is the url", quora_space_url)

        index = 0
        limit = 3  # TODO: Number of followers / 10 (We fetch 10 account per request)
        is_valid_operation = True
        data_to_return = []

        while is_valid_operation:
            curl_command = """ curl --location 'https://shopifyexpert1.quora.com/graphql/gql_para_POST?q=TribeFollowersSocialFirstPagedListQuery' \
                --header 'accept: */*' \
                --header 'accept-language: en-US,en;q=0.9' \
                --header 'content-type: application/json' \
                --header 'cookie: m-b=X19j5pKZE12MmP7prBIlxw==; m-s=JDk4N_vAWAc5eHyeM16qEQ==; m-b_lax=X19j5pKZE12MmP7prBIlxw==; m-b_strict=X19j5pKZE12MmP7prBIlxw==; m-dynamicFontSize=regular; m-themeStrategy=auto; m-theme=dark; m-login=1; m-lat=IH1TB/T3WmWvtmllaYJ4v5FNQlWduIUr7R3z6gHjaw==; m-uid=228910367; m-sa=1; __stripe_mid=3e07c1bc-9fb4-4951-a2a3-f96eb1680188359660; _sharedid=028536c1-05eb-4537-af98-91406b5c460b; m-screen_size=866x925; __gads=ID=d7cb2003ef5dbc53:T=1726607503:RT=1727149989:S=ALNI_MbpPM530aE6nsqkBt_BCj2tQRLffw; __gpi=UID=00000a5156d1dff9:T=1726607503:RT=1727149989:S=ALNI_Mb1ZZBOLlvcgjEJph4RuCbyQUBrCQ; __eoi=ID=e3e25dc29ecd984e:T=1726607503:RT=1727149989:S=AA-AfjYKRqYV5vTPYDH1aql785hY; cto_bundle=tS-W119OZFF4VDBMSFA4UkpjeUFEWVM4eERRZ0ZaU1ZuVUdCdERPRlFEUVlUSVVzJTJCREElMkJFSUIlMkJJbktkZlBaJTJCRmVtVHd5RmprSXBib3JwdTh3c3VSOElIVyUyRjM2Y2ZnbUNnMWxtNXhGeVNZNHVXTk5HYXpFV25aVHljSkhxa1RJc3ZlZTBqNzAyMUh0dXkwdHZadWJoandFdXR6ZTVqZWNVaERFTHlSRE5CampJJTJCMDFOQnBnM0U4Z3ZPWDZtU1ZLTHclMkJPMw; cto_bidid=0z9ohF9NMjVqczhWWTgyJTJCdWZ5ZHdMWmtza2JrOEdIaTBUSnJuSGZyMSUyQno4VUY4elZ2M1JCbWF6dnMwSXlCTVp0eHclMkI5eHc2ZmdrNzBld1ZhcTlGdDFsdllsUHBPVDVGQW5vMXZOR0I1eEhTaVVSTnpNbDhzdVAxRlMyRkl4eFdqU01QcWRSJTJCb1p0dk1IaXpjV0xWeDA5VTBydyUzRCUzRA; __stripe_sid=80290498-ece6-43dc-9906-b452f4ca8114092ef8' \
                --header 'origin: https://shopifyexpert1.quora.com' \
                --header 'priority: u=1, i' \
                --header 'quora-broadcast-id: main-w-chan65-8888-react_cxvntpmhfqwskjwv-WyVQ' \
                --header 'quora-canary-revision: false' \
                --header 'quora-formkey: 70f70e719f28a1fb89ee3c1014bc2b35' \
                --header 'quora-page-creation-time: 1727150155427358' \
                --header 'quora-revision: 34fdbab78dffb8359989920976565945ef13f659' \
                --header 'quora-window-id: react_cxvntpmhfqwskjwv' \
                --header 'referer: https://shopifyexpert1.quora.com/' \
                --header 'referrer-policy: strict-origin-when-cross-origin' \
                --header 'sec-ch-ua: "Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"' \
                --header 'sec-ch-ua-mobile: ?1' \
                --header 'sec-ch-ua-platform: "Android"' \
                --header 'sec-fetch-dest: empty' \
                --header 'sec-fetch-mode: cors' \
                --header 'sec-fetch-site: same-origin' \
                --header 'user-agent: Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36' \
                --data '{"queryName":"TribeFollowersSocialFirstPagedListQuery","variables":{"tribeId":3987924,"first":10,"after":\"""" + str(
                index) + """\","permissions":["follower"],"socialFirst":true},"extensions":{"hash":"4157978ce838c8661e0cc1eb8b9b179b186c26e24c01858f7098f950a615d6a6"}}'
                        """

            # Runs curl command in python subprocess (NOTE: Cannot use python requests - it breaks the request)
            p = subprocess.Popen(curl_command, shell=True, executable='/bin/bash', stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            output, status = p.communicate()

            # Saves user data to data_to_return dict
            json_response = json.loads(output)
            list_of_nodes = json_response.get("data", {}).get("tribe", {}).get("tribeFollowersSocialFirstConnection",
                                                                               {}).get("edges", [])
            for node in list_of_nodes:
                node_data = node.get("node", {})
                print("This is the node", node_data)

                user_info = node_data.get("user", {})
                user_id = user_info.get("uid", 0)
                is_anon = user_info.get("isAnon", False)
                follower_count = user_info.get("followerCount", 0)
                temp_dict = {
                    "user_id": user_id,
                    "is_anon": "1" if is_anon else "0",
                    "follower_count": follower_count
                }
                data_to_return.append(temp_dict)

            if index >= limit:
                is_valid_operation = False
                break

            # Updates index and checks if we need to sleep
            index += 1
            if index % 5 == 0:  # Sleeps after 5 iterations
                sleep(120)

        # Saves all users to quora_users.xlsx - This excel file will be passed into the main function to dispatch follower requests
        df = pd.DataFrame(data_to_return)
        df.to_excel(QuoraScriptHelpers.FILE_NAME_QUORA_USERS, index=True)

        return data_to_return


    @staticmethod
    def dispatch_emails() -> bool:
        """ Dispatches Quora Space follow invites to users in the FILE_NAME_QUORA_USERS file.
            Sleeps every 1-5 minutes.
         """

        # TODO: Open file, loop through each user, and sleep for 1-5 minutes every 20 requests
        df = pd.read_excel(f"./{QuoraScriptHelpers.FILE_NAME_QUORA_USERS}")
        print("This is your df", df)
        return True