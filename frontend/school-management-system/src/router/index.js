import RoleSelect from '../views/roleselect.vue'
import Login from '../views/login.vue'
import update from '../views/update.vue'
import sdashboard from '../views/sdashboard.vue' 
import timetable from '../views/timetable.vue'
import Aaddfaculty from '../views/Aaddfaculty.vue'
import transcript from '../views/transcript.vue'
import Aaddcourse from '../views/Aaddcourse.vue'
import Aremovecourse from '../views/Aremovecourse.vue'
import Alistusers from '../views/Alistusers.vue'
import Aviewcourses from '../views/Aviewcourses.vue'
import Aaddstudent from '../views/Aaddstudent.vue'
import Aremoveuser from '../views/Aremoveuser.vue'
import Ageneratetimetable from '../views/Ageneratetimetable.vue'
import adashboard from '../views/adashboard.vue'
import Fassigngrades from '../views/Fassigngrades.vue'
import Fviewtimetable from '../views/Fviewtimetable.vue'
import FsendNotifications from '../views/FsendNotifications.vue'
import Sadddropcourse from '../views/Sadddropcourse.vue'
import Sviewcourses from '../views/Sviewcourses.vue'

import fdashboard from '../views/fdashboard.vue'
import { createRouter, createWebHistory } from 'vue-router'
const routes = [
  { path: '/', component: RoleSelect },
  { path: '/login', component: Login },
  {path:'/update', component: update},
  {path:'/sdashboard', component: sdashboard},
  {path:'/timetable',component: timetable},
  {path:'/transcript',component: transcript},
  {path:'/Aaddcourse',component:Aaddcourse},
  {path:'/Aremovecourse',component:Aremovecourse},
  {path:'/Aviewcourses',component:Aviewcourses},  
  {path:'/Aaddstudent',component:Aaddstudent},
  {path:'/Aremoveuser',component:Aremoveuser},
  {path:'/Alistusers',component:Alistusers},
  {path:'/Ageneratetimetable',component:Ageneratetimetable},
  {path:'/Fassigngrades', component: Fassigngrades},
  {path:'/Fviewtimetable', component: Fviewtimetable},
  {path:'/Aaddfaculty',component:Aaddfaculty},
    {path:'/adashboard', component: adashboard},
     {path:'/fdashboard', component: fdashboard},
     {path:'/FsendNotifications', component: FsendNotifications},
     {path:'/Sadddropcourse', component: Sadddropcourse},
{path:'/scourses', component: Sviewcourses}

]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
