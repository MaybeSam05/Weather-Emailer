from project import verify, send, weather

def test_verify():
    assert verify("davidmalan@gmail.com") == True
    assert verify("verma.samarth05@gmail.com") == True
    assert verify("blahblah") == False

def test_send():
    assert send("verma.samarth05@gmail.com", "This is the weather report") == "The weather report has been sent to verma.samarth05@gmail.com"
    assert send("davidmalan@gmail.com", "This is the weather report") == "The weather report has been sent to davidmalan@gmail.com"

def test_weather():
    result = weather()
    assert weather(result, str)
