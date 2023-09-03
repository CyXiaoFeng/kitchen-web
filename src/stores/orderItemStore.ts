import { defineStore } from 'pinia';

export const useOrderItemStore = defineStore('counter', {
  state: () => ({
    counter: 0,
    tableId: ''
  }),

  getters: {
    doubleCount (state) {
      return state.counter * 2;
    }
  },

  actions: {
    increment () {
      this.counter++;
    },
    updateTableId(id:string) {
      this.tableId = id
    }

  }
});
