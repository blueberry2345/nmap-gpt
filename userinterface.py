import tkinter
import nmap_scanner
from gpt import api_key_valid
class UserInterface:
    def __init__(self, window):
        # set window
        self.window = window
        # Set title for window
        self.window.title("NMAP-GPT")
        # Set minimum size of window
        self.window.minsize(width=500, height=300)
        # Establish grid for window
        self.window.grid()
        # Make IP and nmap labels
        self.ip_label = tkinter.Label(self.window, text="IP")
        self.nmap_label = tkinter.Label(self.window, text="Nmap")
        self.ip_input = tkinter.Entry(window)
        # Creates button to start nmap scan
        self.submit_button = tkinter.Button(window, text="start", command=self.nmap_scan)
        # Button that clears nmap scan results
        self.clear_button = tkinter.Button(window, text="Clear", command=self.clear_results)
        # Label that displays status and error messages
        self.status_label = tkinter.Label(self.window, text="")


        # Labels for the nmap result table
        self.port_label = tkinter.Label(self.window, text="Port", bg="dark grey")
        self.state_label = tkinter.Label(self.window, text="State", bg="dark grey")
        self.product_label = tkinter.Label(self.window, text="Product", bg="dark grey")
        self.exploit_label = tkinter.Label(self.window, text="Exploits", bg="dark grey")

        # Assign labels and buttons to grid
        self.ip_label.grid(row=0, column=1)
        self.nmap_label.grid(row=1, column=0)
        self.ip_input.grid(row=1, column=1)
        self.submit_button.grid(row=1, column=2)
        self.clear_button.grid(row=1, column=3)
        self.status_label.grid(row=2, column=1)
        self.port_label.grid(row=3, column=0)
        self.state_label.grid(row=3, column=1)
        self.product_label.grid(row=3, column=2)
        self.exploit_label.grid(row=3, column=3)


        # set length of columns
        for x in range(4):
            self.window.grid_columnconfigure(x, minsize=100)

        # store results and labels for results
        self.results = []
        self.result_labels = []

    # Function that does a nmap scan
    def nmap_scan(self):

        # get nmap to scan from input box
        nmap_ip = self.ip_input.get()

        # if nmap input box is not empty
        if nmap_ip:
            # Make submit button text blank
            self.submit_button.config(text="")

            #display status message
            self.status_label.config(text="loading...")

            # run nmap scan
            r = nmap_scanner.run_nmap(nmap_ip)

            # clear existing results table and enter in new data
            self.clear_results()
            self.update_results(r)

            # reverse change of button text as scan is now completed
            self.submit_button.config(text="Submit")

            # If api key invalid then display error message
            if not api_key_valid():
                self.status_label.config(text="Error: API key invalid. Unable to generate exploits")


        # if nmap input box is empty then display error message
        else:
            self.status_label.config(text="Error: IP field is empty")


    # Function that clears all results of the nmap table
    def clear_results(self):
        for row in self.result_labels:
            for result in row:
                result.destroy()
        self.result_labels = []

    # Function that displays results of nmap scan
    def update_results(self, results):
        # If result isn't a string (string type would indicate an error has occurred)
        if not (isinstance(results, str)):
            # set results
            self.results = results
            # set counter
            table_row_counter = 0
            # display the scan results in the table
            for result in self.results:
                port_result_column = tkinter.Label(self.window, text=f"{result['Port']}")
                state_result_column = tkinter.Label(self.window, text=f"{result['State']}")
                product_result_column = tkinter.Label(self.window, text=f"{result['Product']}")
                # version_result_column = tkinter.Label(self.window, text=f"{result['Version']}")
                exploit_result_column = tkinter.Label(self.window, text=f"{result['Exploits']}")

                port_result_column.grid(row=(4 + table_row_counter), column=0)
                state_result_column.grid(row=(4 + table_row_counter), column=1)
                product_result_column.grid(row=(4 + table_row_counter), column=2)
                exploit_result_column.grid(row=(4 + table_row_counter), column=3)
                table_row_counter += 1

                # add row of labels to list
                self.result_labels.append(
                    [port_result_column, state_result_column, product_result_column, exploit_result_column])
            # reset status message
            self.status_label.config(text="")

        # display error message if result is type String
        else:
            self.status_label.config(text=results)
