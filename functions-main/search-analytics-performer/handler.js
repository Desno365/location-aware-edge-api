"use strict";

// Dependencies.
const edgeDb = require("./common/edge-db/edgeDb");

module.exports = async (event, context) => {
  const latestSearchesList = await edgeDb.getList("latest_searches_list");
  console.log("Latest searches list: " + latestSearchesList);

  const trendingSearches = await getTrendingSearches(latestSearchesList);

  return context
      .status(200)
      .succeed(trendingSearches);
}

async function getTrendingSearches(latestSearchesList) {
  return sortByFrequencyAndRemoveDuplicates(latestSearchesList);
}

function sortByFrequencyAndRemoveDuplicates(array) {
  let frequency = {}, value;

  // compute frequencies of each value
  for(let i = 0; i < array.length; i++) {
    value = array[i];
    if(value in frequency) {
      frequency[value]++;
    }
    else {
      frequency[value] = 1;
    }
  }

  // make array from the frequency object to de-duplicate
  let uniques = [];
  for(const value in frequency) {
    uniques.push(value);
  }

  // sort the uniques array in descending order by frequency
  function compareFrequency(a, b) {
    return frequency[b] - frequency[a];
  }

  return uniques.sort(compareFrequency);
}
