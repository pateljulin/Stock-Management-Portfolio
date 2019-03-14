import os
import robin_stocks


class Portfolio:

    def __init__(self, first_name, last_name):
        """
        Initializes the class with user portfolio information
        :param first_name: first name of user
        :param last_name:  last name of user
        """
        self.__first_name = str(first_name)
        self.__last_name = str(last_name)
        self.__full_name = first_name + last_name
        # Create file path for users portfolio
        self.__file_path = self.__full_name + "_portfolio.txt"
        self.stock_tick_opt = dict()
        self.stock_tick_avg = dict()
        self.stock_ticker = ""
        self.options = 0
        self.avg_cost = 0

        try:
            fp = open(self.__file_path, "r")
            current_stock = [line.split() for line in fp]
            for i in range(len(current_stock)):
                self.stock_tick_opt[current_stock[i][0]] = float(current_stock[i][1])
                self.stock_tick_avg[current_stock[i][0]] = float(current_stock[i][2])

        except IOError:
            # If not exists, create the file
            fp = open(self.__file_path, 'w+')
            fp.close()

    def get_file_path(self):
        return self.__file_path

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_stock_opt(self):
        return self.stock_tick_opt

    def get_stock_avg(self):
        return self.stock_tick_avg

    def add_stock(self, ticker, num_options, num_avg_cost):
        """
        Add a specific stock to users portfolio
        :param ticker: Stock ticker
        :param num_options: Number of shares
        :param num_avg_cost: the average cost per share
        :return: 2 Separate dictionaries one with ticker as key and number of shares as values
                second one with ticker as key and avg cost as value
        """
        self.stock_ticker = ticker
        self.options = float(num_options)
        self.avg_cost = float(num_avg_cost)

        # If user does not own stock in the company add to users lists
        if self.stock_ticker not in self.stock_tick_opt.keys():
            self.stock_tick_opt[self.stock_ticker] = self.options
            self.stock_tick_avg[self.stock_ticker] = self.avg_cost
        else:
            # Get most up to date avg cost
            self.stock_tick_avg[self.stock_ticker] = (((self.stock_tick_avg[self.stock_ticker] * self.stock_tick_opt[self.stock_ticker]) +
                                                   (self.avg_cost * self.options)) / (self.stock_tick_opt[self.stock_ticker] + self.options))
            self.stock_tick_opt[self.stock_ticker] += self.options

        # Insert shares into Users portfolio text file
        try:
            fp = open(self.__file_path, "w")
            for val in self.stock_tick_opt.keys():
                fp.write('{:1s} {:1s} {:1s}'.format(val, format(float(self.stock_tick_opt[val]), ".2f"), format(float(self.stock_tick_avg[val]), ".2f") + "\n"))
            fp.close()
            return self.stock_tick_opt, self.stock_tick_avg
        except IOError:
            # If not exists, create the file
            fp = open(self.__file_path, 'w+')
            fp.close()

    def __add_stock_from_robinhood(self, robinhood_dict):
        """
        function adds stocks imported from Robinhood into users portfolio
        :param robinhood_dict: dictionary of stock tickers with values in a list of number of shares and avg cost

        """
        for key in robinhood_dict.keys():
            self.stock_ticker = key
            self.options = float(robinhood_dict[key][0])
            self.avg_cost = float(robinhood_dict[key][1])
            # If user does not own shares of a company, add them to list
            if self.stock_ticker not in self.stock_tick_opt.keys():
                self.stock_tick_opt[self.stock_ticker] = self.options
                self.stock_tick_avg[self.stock_ticker] = self.avg_cost
            else:
                # Get most up to date avg cost
                self.stock_tick_avg[self.stock_ticker] = (
                            ((self.stock_tick_avg[self.stock_ticker] * self.stock_tick_opt[self.stock_ticker]) +
                             (self.avg_cost * self.options)) / (self.stock_tick_opt[self.stock_ticker] + self.options))
                self.stock_tick_opt[self.stock_ticker] += self.options

        # Add stocks to users on going text file of shares
        try:
            fp = open(self.__file_path, "w")
            for key in self.stock_tick_opt.keys():
                fp.write('{:1s} {:1s} {:1s}'.format(key, format(float(self.stock_tick_opt[key]), ".2f"),
                                                    format(float(self.stock_tick_avg[key]), ".2f") + "\n"))
            fp.close()
        except IOError:
            # If not exists, create the file
            fp = open(self.__file_path, 'w+')

    def sell_stock(self, ticker, num_options):
        """
        If user sells stock, update users current ongoing manager
        :param ticker: Stock ticker user is selling
        :param num_options: Number of options user is selling
        :return: Prints the sell price of the stock ticker (based on the user selling it right at the moment of updating
                 portfolio)
        """
        self.stock_ticker = ticker
        self.options = float(num_options)

        # If the user does not own any of those shares
        if self.stock_ticker not in self.stock_tick_opt.keys():
            print("You do not currently hold any shares of {}.".format(self.stock_ticker))
        else:
            # Adjust new number of shares owned by user
            self.stock_tick_opt[self.stock_ticker] -= self.options

            # If user now owns 0 stock of that company. Remove from portfolio
            if self.stock_tick_opt[self.stock_ticker] == 0.0:
                self.stock_tick_opt.pop(self.stock_ticker)

            fp = open(self.__file_path, "w")
            # Readjust user portfolio text
            for val in self.stock_tick_opt.keys():
                fp.write('{:1s} {:1s} {:1s}'.format(val, str(self.stock_tick_opt[val]),
                                                    format(float(self.stock_tick_avg[val]), ".2f")) + "\n")
            fp.close()
            try:
                print("Your sell price for {} was: $".format(ticker),
                      format(float(robin_stocks.stocks.get_latest_price(ticker)[0]), ".2f"))
            except Exception as e:
                print(e, "Live sell price no available. Please get Robinhood account to access live price.")

    def get_portfolio(self):
        """
        :return:  prints out users portfolio in terminal
        """
        try:
            if os.path.isfile(self.__file_path):
                if os.stat(self.__file_path).st_size == 0:
                    print("Your portfolio is currently empty. Please add stocks.")
                else:
                    fp = open(self.__file_path, "r")
                    for lines in fp.readlines():
                        print(lines)
        except Exception as e:
            print(e, "No File Found.")

    def get_robin_data(self, username, password):
        """
        :param username: enter robinhood username
        :param password: enter robinhood password
        :return: a dictionary of your Robinhood stocks
        """
        try:
            # Creates a connection with Robinhood
            login = robin_stocks.login(username, password)
        except Exception as e:
            print(e, "Username or Password is incorrect.")

        # Pulls in user portfolio data from Robinhood
        my_stocks = robin_stocks.build_holdings()
        robinhood_dict = dict()
        # Extracts Ticker symbols as well as quantity of each ticker and average buy price of that ticker
        # Store that data in a list
        for key, value in my_stocks.items():
            robinhood_dict[key] = [value['quantity'], value['average_buy_price']]
        # Add stock to portfolio text file
        self.__add_stock_from_robinhood(robinhood_dict)
        return robinhood_dict

    def __repr__(self):
        return "This portfolio belongs to %s %s ".format(self.__first_name, self.__last_name)
