function makePostRequest(path, btn) {
    return new Promise(function (resolve, reject) {

      const data =  {
        "operationName": "GetAxieBriefList",
        "variables": {
          "from": 0,
          "size": 24,
          "sort": "PriceAsc",
          "auctionType": "All",
          "owner":"0xace0e8c06d5143e3ff4e8b3400e38253595dd3ed",
          "criteria": {}
        },
        "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
      }
      fetch(path,{
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      })
      .then((response)=> {
        return response.json();
      })
      .then((data) => {
          url_ = 'http://localhost:2358//submissions/' + data.token + '?base64_encoded=false&fields';
          if(btn == 'run')
            jQuery('#result').html('Processing...');
          else if(btn == 'submit')
            jQuery('#submit').html("<div class='footer text-center mt-4'>Processing...</div>");
          resolve(url_);
        },
          (error) => {
          reject(error);
        }
      );
    });
  }

  var path = 'https://graphql-gateway.axieinfinity.com/graphql';

  var ans = makePostRequest(path);