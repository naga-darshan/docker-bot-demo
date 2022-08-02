Feature:
  This feature will let the user retrieve information and details from the spot exchange's public API
  and validate them using API

  @test @publicapi @firstTest
  Scenario: Test scenario 1
    Given I am connected to spot exchange "public" api
    When I retrieve the server time
    Then validate the api response
    And Response "status" is "equal to" "200"
    And Response "time" is "less than" "500"
    And Response "header" has "[{'Content-Type':'application/json'}, {'Server':'cloudflare'}]"
    And Response "body" has "[{'result.unixtime':'non-zero-number'}]"


  @test @publicapi
  Scenario: Test scenario 2
    Given I am connected to spot exchange "public" api
    When I retrieve the "XBT/USD" trade pair
    Then validate the api response
    And Response "status" is "equal to" "200"
    And Response "time" is "less than" "500"
    And Response "header" has "[{'Content-Type':'application/json; charset=utf-8'}, {'Server':'cloudflare'}]"

