from time import sleep

from helpers.quora_script_helpers import QuoraScriptHelpers


class QuoraScript:
    """ Class to run the quora bot """

    def run(self) -> bool:
        """ Runs the main process. """

        temp_response = QuoraScriptHelpers.send_invite(user_id="228910367")
        print("This is the resposne", temp_response)
        return temp_response

        # email_dispatch_response = QuoraScriptHelpers.dispatch_invites()
        # print("Ran the process with a response of", email_dispatch_response)
        # return email_dispatch_response


if __name__ == "__main__":
    email_script = QuoraScript()
    email_script.run()
