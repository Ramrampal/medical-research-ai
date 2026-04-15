const axios = require('axios');

class OpenAlexService {
  constructor() {
    this.baseURL = 'https://api.openalex.org/';
  }

  async searchByDisease(disease, query) {
    try {
      const response = await axios.get(`${this.baseURL}works?filter=concepts.wikipedia:${disease},title:${query}`);
      return response.data;
    } catch (error) {
      console.error('Error fetching data from OpenAlex API:', error);
      throw error;
    }
  }
}

module.exports = new OpenAlexService();
