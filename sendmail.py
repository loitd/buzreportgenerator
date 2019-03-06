from zeep import Client

def test():
    client = Client('http://www.dneonline.com/calculator.asmx?wsdl')
    result = client.service.Add(100,220)
    print(result)

def test2():
    client = Client('http://172.16.237.11:8080/SendNotify_Interface_Gmail/services/Notify?wsdl')
    result = client.service.sendEmail("loitd@vnptepay.com.vn", "deglkxtfyjpnjqtq", "Ahihi", "Xin chao", "loitd@vnptepay.com.vn", 1)
    print(result)

if __name__ == "__main__":
    test2()