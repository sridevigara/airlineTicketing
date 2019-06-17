from autoLoad import *

class search:

    ## Getting Airport IATA (International Air Transport Association)
    def getAirport(self,fromStation):
        try:
            self.fromStation = str(fromStation)
            result = DBActivity.db.query("select name as apname, iata,apid from airports ap "
                                         "where ap.city = '"+self.fromStation+"' and ap.iata!= ''")
            if result['count'] not in [-1, 0]:
                return result['data']
            else:
                print("No Airport found with given name "+self.fromStation)
                sys.exit()

        except mysqlDB.Error as err:
            print("Something went wrong: {}".format(err))


    def getFlights(self,inputData):
        try:
            # select rt.*,arl.* from routes rt, airlines arl,flights fl where rt.alid = arl.alid and
            # fl.route_id=rt.rid  and rt.src_ap='bom' and rt.dst_ap='del' and fl.start_date>='2019-06-27'
            # and fl.end_date<='2019-06-27' and fl.available_seats>0

            queryStr = "select rt.*, arl.name as airline_name, fl.* " \
                    "from routes rt" \
                    ", airlines arl " \
                    ", flights fl " \
                    "where " \
                    "rt.alid= arl.alid " \
                    "and fl.route_id= rt.rid " \
                    "and arl.active= 'Y'" \
                    "and rt.src_ap='" + inputData['fromIata'] + "' " \
                    "and rt.dst_ap='" + inputData['toIata'] + "' " \
                    "and fl.start_date>= '"+inputData['travelDate']+"' " \
                    "and fl.end_date<= '"+inputData['travelEndDate']+"' " \
                    "and fl.available_seats>= '"+inputData['passengerCnt']+"' "
            result = DBActivity.db.query(queryStr)
            if result['count'] not in [-1, 0]:
                return result['data']
            else:
                print("No Flights available with given data!... ")
                sys.exit()

        except mysqlDB.Error as err:
            print("Something went wrong: {}".format(err))



