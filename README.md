# Client Invoice Generator (CIG)
Simple client invoice generator, created in late 2022 - early 2023.

Uses CherryPy for the web framework. Web content is displayed and updated using templates.

## Pages
The homepage links to three pages: Clients, Generate Invoice, and Invoice History.

![Homepage](/images/homepage_1.png "Homepage")

The Clients page displays client data read from the company database and formats it in a table. 

![Clients Page](/images/clientspage.png "Clients Page")

The Generate Invoice page allows the user to select fields such as client, hourly rate etc. and generates an invoice based on these when the user clicks the 'generate' button.

![Generate Invoice](/images/generateinvoice.png "Generate Invoice Page")
<img src="/images/invoiceexample.png" alt="Example of a Generated Invoice" title="Example of a Generated Invoice" width="60%"/>

The user can choose to save the invoice to invoice history, and in that case, it is updated on the Invoice History page.

![Invoice History Page](/images/invoicehistory.png "Invoice History Page")
