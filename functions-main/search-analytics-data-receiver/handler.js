"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edge-db");

// Constants.
const trendingSearchesDataDomain = { referringAreaType: "country", ttl: 4*60*60*1000 }; // 4 hours TTL.

module.exports = async (event, context) => {
  const searchData = event.body.search_data.toLowerCase();
  const response = await edgeDb
      .withDataDomain(trendingSearchesDataDomain)
      .addToList("latest_searches_list", searchData);
  return context
      .status(200)
      .succeed(response);
}
