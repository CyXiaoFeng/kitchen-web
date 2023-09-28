export default {
  data () {
    return {

    }
  },
  methods: {
    resMsg(res) {
      const regex = /\{([^}]+)\}/g;
      if (regex.test(res)) {
        const replacedStr = res.replace(regex, (match, p1)=> {
          return "${this.$t('" + p1 + "')}";
        });
        return eval("`"+replacedStr+"`");
      } else {
        return res
      }
      
    },
    goPage (val) {
      this.$router.push(val)
    },
    checkStringNull (val) {
      if (val === null || val.length < 1) {
        return true
      }
      return false
    },
    getBaseServiceUrl () {
      this.$api.get('/base-service').then(response => {
        this.base_service_url = response.data
        console.log(this.base_service_url)
      }).catch(e => {
        this.notifyFail('获取base service url失败')
      })
    },
    notifySuccess (message) {
      this.$q.notify({
        color: 'green',
        textColor: 'white',
        icon: 'thumb_up',
        message: message,
        position: 'top-right',
        avatar: 'statics/huaji.png'
      })
    },
    notifyWarn (message) {
      this.$q.notify({
        color: 'orange',
        textColor: 'white',
        icon: 'thumb_up',
        message: message,
        position: 'top-right',
        avatar: 'statics/sad.png'
      })
    },
    notifyFail (message) {
      this.$q.notify({
        color: 'red',
        textColor: 'white',
        icon: 'thumb_up',
        message: message,
        position: 'top-right',
        avatar: 'statics/sad.png'
      })
    }
  }
}
