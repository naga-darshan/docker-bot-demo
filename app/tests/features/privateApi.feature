Feature:
  This feature will let the user retrieve information and details from the spot exchange's private API
  and validate them using API

  @test @privateapi
  Scenario: Test scenario 3
    Given I am connected to spot exchange "private" api
    When I retrieve the "open" orders for the account
    Then validate the api response
    And Response "status" is "equal to" "200"
    And Response "time" is "less than" "500"
    And Response "header" has "[{'Content-Type':'application/json'}, {'Server':'cloudflare'}]"
    And Response "body" has "[{'result.open.status':'pending'}]"