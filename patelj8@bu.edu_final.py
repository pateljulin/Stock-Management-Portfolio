from Portfolio import Portfolio
import getpass


def main():
    fl_name = True
    while fl_name:
        print("Welcome! Lets start by creating your portfolio: \n")
        first_name = input("Please enter your first name: ")
        first = True
        while first:
            for char in first_name:
                if not char.isalpha():
                    print("Please enter only Alpha characters. \n")
                    first_name = input("Please enter your first name: ")
                else:
                    first = False
        last_name = input("Please enter your last name: ")
        last = True
        while last:
            for char in last_name:
                if not char.isalpha():
                    print("Please enter only Alpha characters. \n")
                    last_name = input("Please enter your last name: ")
                else:
                    last = False

        new_portfolio = Portfolio(first_name, last_name)
        fl_name = False
        main_menu = True
        while main_menu:
            print("Main Menu: \n")
            print("1. Manually Add a Stock \n")
            print("2. Manually Sell a Stock \n")
            print("3. Import stock profile from Robinhood \n")
            print("4. View Portfolio \n")
            print("5. Exit Program \n")

            try:
                user_selection = int(input("Selection: "))
                if user_selection == 1:
                    ticker = input("Please enter in ticker symbol: ")
                    num_shares = input("Please enter in number of share(s): ")
                    avg_cost = input("Please enter in the average cost per share: ")
                    new_portfolio.add_stock(ticker, num_shares, avg_cost)
                elif user_selection == 2:
                    ticker = input("Please enter in ticker symbol: ")
                    num_shares = input("Please enter in number of share(s): ")
                    new_portfolio.sell_stock(ticker, num_shares)
                elif user_selection == 3:
                    username = input("Please enter your Robinhood account username: ")
                    try:
                        password = getpass.getpass()
                    except Exception as e:
                        print(e, " Password Error!")
                    try:
                        new_portfolio.get_robin_data(username, str(password))
                    except Exception as e:
                        print(e, "Account information invalid. \n")
                elif user_selection == 4:
                    new_portfolio.get_portfolio()
                elif user_selection == 5:
                    print("Thank You for using this program! \n")
                    break
                else:
                    print("Your input is incorrect. \n")
            except Exception as e:
                print(e, "Incorrect input")


if __name__ == '__main__':
    main()
