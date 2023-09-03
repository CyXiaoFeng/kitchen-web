import { boot } from 'quasar/wrappers';
import { createPinia } from 'pinia';
import { useOrderItemStore } from 'stores/orderItemStore'
export const pinia = createPinia();
const store = useOrderItemStore()
export default boot(({ app }) => {
  app.config.globalProperties.$store = store
  console.log("info from boot store" +　store.tableId)
});
export { store }