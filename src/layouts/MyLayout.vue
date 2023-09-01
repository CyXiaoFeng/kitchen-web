/* eslint-disable */
<template>
  <q-layout view="lHh Lpr lFf">
    <q-header>
      <q-toolbar color="primary">
        <q-btn
          v-if="loggedIn"
          flat
          dense
          round
          icon="menu"
          aria-label="Menu"
          @click="leftDrawerOpen = !leftDrawerOpen"
        />

        <q-toolbar-title>
          <a @click="goPage('/')" style="cursor: pointer">小厨</a>
          <div>厨房点菜一体化系统</div>
        </q-toolbar-title>
        <q-btn-dropdown flat :label="user">
          <q-list link>
            <q-item v-if="loggedIn" clickable @click="goPage('/change-pass')">
              <q-item-section> 修改密码 </q-item-section>
              <q-item-section side right icon="info" color="amber" />
            </q-item>

            <q-item v-if="loggedIn" clickable @click="logout">
              <q-item-section> 登出 </q-item-section>
              <q-item-section avatar>
                <q-icon side right name="info" />
              </q-item-section>
            </q-item>
            <q-item v-if="!loggedIn" clickable @click="goPage('/login')">
              <q-item-section> 登录 </q-item-section>
              <q-item-section avatar>
                <q-icon side right name="info" />
              </q-item-section>
            </q-item>
          </q-list>
        </q-btn-dropdown>
      </q-toolbar>
    </q-header>

    <q-drawer
      v-model="leftDrawerOpen"
      :content-class="$q.theme === 'mat' ? 'bg-grey-2' : null"
    >
      <q-list no-border link inset-delimiter>
        <q-item-label header>功能菜单</q-item-label>
        <q-item
          clickable
          v-ripple
          v-if="my_role === '管理员'"
          @click="goPage('/dish-manage')"
        >
          <q-item-section avatar>
            <q-icon name="fastfood" />
          </q-item-section>
          <q-item-section>菜品管理</q-item-section>
        </q-item>
        <q-item
          clickable
          v-ripple
          v-if="my_role === '管理员'"
          @click="goPage('/table-manage')"
        >
          <q-item-section avatar>
            <q-icon name="table_chart" />
          </q-item-section>
          <q-item-section>餐桌管理</q-item-section>
        </q-item>
        <q-item
          clickable
          v-ripple
          v-if="my_role === '管理员'"
          @click="goPage('/kitchen-manage')"
        >
          <q-item-section avatar>
            <q-icon name="smoking_rooms" />
          </q-item-section>
          <q-item-section>厨房管理</q-item-section>
        </q-item>
        <q-expansion-item
          v-if="my_role === '服务员' || my_role === '管理员'"
          indent
          icon="recent_actors"
          label="服务员视图"
          default-opened
        >
          <q-item
            clickable
            inset-level="1"
            class="main-item"
            @click="goPage('/order-manage')"
          >
            <q-item-section avatar>
              <q-icon name="menu" />
            </q-item-section>
            <q-item-section>进行中订单</q-item-section>
          </q-item>
          <q-item
            clickable
            inset-level="1"
            class="main-item"
            @click="goPage('/order-by-table')"
          >
            <q-item-section avatar>
              <q-icon name="crop_din" />
            </q-item-section>
            <q-item-section>餐桌视图</q-item-section>
          </q-item>
        </q-expansion-item>
        <q-expansion-item
          v-if="my_role === '厨师' || my_role === '管理员'"
          indent
          icon="assignment_ind"
          label="厨师视图"
          default-opened
        >
          <q-item
            clickable
            inset-level="1"
            class="main-item"
            @click="goPage('/chef-assignment-board')"
          >
            <q-item-section avatar>
              <q-icon name="assignment" />
            </q-item-section>
            <q-item-section>点菜分配视图</q-item-section>
          </q-item>
        </q-expansion-item>
        <q-expansion-item
          v-if="my_role === '管理员'"
          indent
          icon="recent_actors"
          label="报表管理"
          default-opened
        >
          <q-item
            clickable
            inset-level="1"
            class="main-item"
            @click="goPage('/report-manage')"
          >
            <q-item-section avatar>
              <q-icon name="wallpaper" />
            </q-item-section>
            <q-item-section>全部历史订单</q-item-section>
          </q-item>
          <q-item
            clickable
            inset-level="1"
            class="main-item"
            @click="goPage('/report-by-table')"
          >
            <q-item-section avatar>
              <q-icon name="tablet" />
            </q-item-section>
            <q-item-section>历史订单(餐桌)</q-item-section>
          </q-item>
        </q-expansion-item>

        <q-item
          clickable
          v-if="my_role === '管理员'"
          class="main-item"
          @click="goPage('/user-manage')"
        >
          <q-item-section avatar>
            <q-icon name="people" />
          </q-item-section>
          <q-item-section>用户管理</q-item-section>
        </q-item>
      </q-list>
    </q-drawer>

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>

<script>
import { openURL } from "quasar"

export default {
  name: "MyLayout",
  interval: null,
  data() {
    return {
      user: "用户",
      my_role: "",
      loggedIn: false,
      leftDrawerOpen: true,
    }
  },
  methods: {
    openURL,
    goPage(val) {
      this.$router.push(val)
    },
    logout() {
      this.$api
        .post(
          "/logout",
          {},
          { headers: { "Content-Type": "application/x-www-form-urlencoded" } }
        )
        .then((response) => {
          location.reload()
        })
        .catch((e) => {
          location.reload()
        })
    },
    whoami() {
      this.$api
        .get("/api/v1/user/info")
        .then((response) => {
          console.info("return" + response.data)
          this.user = response.data.username
          this.loggedIn = true
          this.my_role = response.data.role_name
          clearInterval(this.interval)
        })
        .catch((error) => {
          clearInterval(this.interval)
          console.log(error)
          this.leftDrawerOpen = false
          this.loggedIn = false
          this.$router.push("/login")
        })
    },
    regularCheckLogin() {
      var count = 0
      this.interval = setInterval(() => {
        count = count + 1
        this.whoami()
      }, 15000)
    },
  },
  mounted() {
    this.leftDrawerOpen = this.loggedIn && this.$q.platform.is.desktop
    this.whoami()
    this.regularCheckLogin()
  },
}
</script>

<style>
.main-item {
  cursor: pointer;
}
</style>
