from autoLoad import *
from search import *
from booking import *

searchObj = search()

# From Airport
#"mumbai"
fromStation = input("Please Enter From Station ")
fromStationData = searchObj.getAirport(fromStation)
fromIata = fromStationData[0]['iata']

# To Airport
#"delhi"
toStation = input("Please Enter To Station ")
toStationData = searchObj.getAirport(toStation)
toIata = toStationData[0]['iata']

# Travelling Date
# "2019-06-25"
travelDate = input("Please Enter Travel Date in yyyy-mm-dd ")
if not validate(travelDate):
    print("Incorrect Travelling Date "+travelDate)
    sys.exit()
travelEndDate = travelDate


# Flexible Date
travelDateFelxible = input("Please Enter Travel Date Flexibity of 7 days Yes/No ")
if not validateList(travelDateFelxible.lower(), ["yes", "y", "no", "n"]):
    print("Incorrect value " + travelDate+ ", Enter Yes/No")
    sys.exit()
elif validateList(travelDateFelxible.lower(), ["yes", "y"]):
    travelEndDate = (datetime.strptime(travelDate, DATEFORMAT) + timedelta(days=7)).strftime(DATEFORMAT)


# No Of Passengers
passengerCnt = input("Please Enter No Of Passengers ")
if not validateInteger(passengerCnt):
    print("Please enter numbers only")
    sys.exit()
elif int(passengerCnt) <= 0:
    print("Please enter numbers, atleast 1")
    sys.exit()


##inputData = {"fromIata":fromIata, "toIata":toIata, "travelDate":travelDate, "travelEndDate":travelEndDate,
# "travelDateFelxible":travelDateFelxible, "passengerCnt":str(passengerCnt)}
inputData = {"fromIata": "BOM", "toIata": "DEL", "travelDate": "2019-06-25", "travelEndDate": "2019-07-02",
             "travelDateFelxible": "y", "passengerCnt": "2"}

# Get flights information
flightsData = searchObj.getFlights(inputData)
print("Given Data:\n Route: "+fromStation.upper()+" -- "+toStation.upper()+"\n Travel date: "+travelDate+" - "+travelEndDate+"\n No Passengers "+passengerCnt+"\n")
print("Available Flights:\n")

for fdata in flightsData:
    print("Booking ID: " + str(fdata["route_id"]))
    print("Airline: " + fdata["airline_name"])
    print("Departure Date: " + datetime.strftime(fdata["start_date"], DISPLAY_DATEFORMAT))
    #print("Departure Time: " + str(fdata["departure_time"]))
    print("Arrival Date: " + datetime.strftime(fdata["end_date"], DISPLAY_DATEFORMAT))
    #print("Arrival Time: " + fdata["arrival_time"])
    #print("Duration: " + fdata["flight_duration"])
    print("Price: " + str(fdata["base_price_usd"]) + "$")
    print("Status: " + fdata["status"] + "\n")

continueBooking = input("Do want to continue booking Yes/No :")
if not validateList(continueBooking.lower(), ["yes", "y", "no", "n"]):
    print("Incorrect value " + continueBooking+ ", Enter Yes/No")
    sys.exit()
elif validateList(continueBooking.lower(), ["yes", "y"]):
    bookingInit = 1
    bookingIds = list(map(lambda x: x["route_id"], flightsData))
    # Displaying the booking IDs for continuing booking
    print("Select booking ID's from below:")
    print(bookingIds)
    #10322
    bookingId = int(input())

    # Getting selected booking ID complete details
    selectedFlighDetails = ([i for i in flightsData if i['route_id'] == bookingId][0])

    if not validateList(bookingId, bookingIds):
        print("Incorrect value " + bookingId)
        sys.exit()
    else:
        # Initiating Booking Process
        allPassengerDetail = []
        """allPassengerDetail = [{'first_name': 'Sridevi',
                               'middle_name': '', 'last_name': 'Gara',
                               'date_of_birth': '1984-06-04', 'gender': 'f',
                               'email': 'sri@gmail.com', 'phone': '8787878989', 'is_primary': '1'},
                              {'first_name': 'Vara', 'middle_name': 'Prasad',
                               'last_name': 'Vanam', 'date_of_birth': '1984-10-09',
                               'gender': 'M', 'email': 'vara@gmail.com', 'phone': '8787676778', 'is_primary': '0'}]"""
        for passenger in range(int(passengerCnt)):
            passengerDetail = dict()
            mandatory = "**Enter Primary" if passenger == 0 else "Enter"
            nonMandatory = "Enter Primary" if passenger == 0 else "Enter"
            isPrimary = "1" if passenger == 0 else "0"
            passengerDetail['first_name'] = input("{} Passenger{} First Name: ".format(mandatory, str(passenger+1)))
            passengerDetail['middle_name'] = input("{} Passenger{} Middle Name: ".format(nonMandatory, str(passenger+1)))
            passengerDetail['last_name'] = input("{} Passenger{} Last Name: ".format(mandatory, str(passenger+1)))
            passengerDetail['date_of_birth'] = input("{} Passenger{} Date Of Birth: ".format(mandatory, str(passenger+1)))
            passengerDetail['gender'] = input("{} Passenger{} Gender(female/male): ".format(mandatory, str(passenger+1)))
            passengerDetail['email'] = input("{} Passenger{} Email: ".format(mandatory, str(passenger+1)))
            passengerDetail['phone'] = input("{} Passenger{} Phone Number: ".format(mandatory, str(passenger+1)))
            passengerDetail['is_primary'] = isPrimary
            allPassengerDetail.append(passengerDetail)

        ##print(allPassengerDetail)
        bookingInit = booking()
        bookingInit.initBooking(selectedFlighDetails, allPassengerDetail, passengerCnt)

