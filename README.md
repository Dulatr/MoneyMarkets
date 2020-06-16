# MoneyMarketCLI

This script retrieves and stores the quoted prices for the DOW, Nasdaq and S&P 500 from the [CNN money markets](https://money.cnn.com/data/markets/). Retrieved data is stored in the JSON format for a file specified by the user prompt.

# Requirements

* [Selenium](https://selenium-python.readthedocs.io/installation.html)

# Install

For windows users using cxFreeze you can create an executable via [setup.py](setup.py):

```powershell
# Clone the repo
git clone https://github.com/Dulatr/MoneyMarketsCLI
cd MoneyMarketsCLI

# Install cxFreeze
pip install cx_Freeze --upgrade
pip install -r requirements.txt

# Run the build
python ./setup.py build

# Add to path
$Env:Path += ";./build/exe.<your exe version folder>/"

# use!
./money.exe stock --help
```
For detailed usage read this [statement](https://github.com/Dulatr/MoneyMarketsCLI/pull/5).