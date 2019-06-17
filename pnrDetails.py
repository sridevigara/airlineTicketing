from autoLoad import *

class pnrDetails:

    ## Getting Travel Details based on PNR number
    def validatePnr(self,pnrNumber):
        try:
            self.pnrNumber = str(pnrNumber)
            result = DBActivity.db.query("select bkid from flight_booking  "
                                         "where pnr= '"+self.pnrNumber+"' and txn_status= 'completed' and "
                                         "payment_status= 'completed' ")
            ##print( result)
            if result['count'] not in [-1, 0]:
                return result['count']
            else:
                print("No Travel Details found with given PNR "+self.pnrNumber)
                sys.exit()

        except mysqlDB.Error as err:
            print("Something went wrong: {}".format(err))


    def getPnrDetails(self, pnrNumber):
        try:
            self.pnrNumber = str(pnrNumber)
            queryStr = "select fbkp.*,fbk.amount_usd , al.name as alname, " \
                       "(select city from airports where iata = rt.src_ap ) as from_startion, " \
                       "(select city from airports where iata = rt.dst_ap) as to_startion," \
                       "f.start_date, f.end_date " \
                       "from flight_booking fbk, flight_booking_passenger fbkp, " \
                       "flights f, routes rt, airlines al " \
                       "where  fbk.pnr = fbkp.pnr " \
                       "and fbk.flight_id = f.flid " \
                       "and f.route_id = rt.rid " \
                       "and rt.alid = al.alid " \
                       "and fbk.txn_status = 'completed' " \
                       "and fbk.payment_status = 'completed' " \
                       "and fbk.pnr = '"+self.pnrNumber +"'"
            result = DBActivity.db.query(queryStr)
            print(queryStr)
            if result['count'] not in [-1, 0]:
                return result['data']
            else:
                print("No Flights available with given data!... ")
                sys.exit()

        except mysqlDB.Error as err:
            print("Something went wrong: {}".format(err))


pnrNumber = input("Enter PNR Number: ")
if len(pnrNumber) < PNRLENGTH:
    print("Please enter valid PNR Number")
    sys.exit()
else:
    travelDataObj = pnrDetails()
    resultCnt = travelDataObj.validatePnr(pnrNumber)
    travelData = travelDataObj.getPnrDetails(pnrNumber)
    print("Travel Details: "+ pnrNumber)
    loop = 0
    for passenger in travelData:
        ##print(passenger)
        if loop is 0:
            print("From Station: "+passenger['from_startion'])
            print("To Station: " + passenger['to_startion'])
            print("Airlines: " + passenger['alname'])
            print("Departure Date: " + datetime.strftime(passenger["start_date"], DISPLAY_DATEFORMAT))
            print("Arrival Date: " + datetime.strftime(passenger["end_date"], DISPLAY_DATEFORMAT))
            print("Price: " + str(passenger["amount_usd"]) + "$\n")


        mandatory = "Primary Passenger"+str(loop+1) if loop == 0 else "Passenger"+str(loop+1)
        CB720F2D18E44C0180CD
        print("{} Details: ".format(mandatory))
        print("First  Name: "+passenger['first_name'])
        print("Middle  Name: " + passenger['middle_name'])
        print("Last  Name: " + passenger['last_name'])
        print("Seat Number: " + passenger['seat_number'])
        print("Date Of Birth: " + datetime.strftime(passenger["date_of_birth"], DISPLAY_DATEFORMAT))
        print("Gender: " + passenger['gender'])
        print("Email: " + passenger['email'])
        print("Phone: " + passenger['phone']+"\n")

        loop += 1

