import{_ as p,q as n,k as l,l as c,B as a,M as m,x as _,u as g,y as f}from"./vendor-f0f38b48.js";import"./vendor-sortablejs-cbf37f8f.js";const b={name:"DeviceHuaweiSmartLogger",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},componentId:{required:!0}},methods:{updateConfiguration(t,e=void 0){this.$emit("update:configuration",{value:t,object:e})}}},v={class:"device-huawei-smart-logger"},w={class:"small"};function x(t,e,i,h,q,s){const r=n("openwb-base-heading"),u=n("openwb-base-text-input"),d=n("openwb-base-number-input");return l(),c("div",v,[a(r,null,{default:m(()=>[_(" Einstellungen für Huawei SmartLogger "),g("span",w,"(Modul: "+f(t.$options.name)+")",1)]),_:1}),a(u,{title:"IP oder Hostname",subtype:"host",required:"","model-value":i.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=o=>s.updateConfiguration(o,"configuration.ip_address"))},null,8,["model-value"]),a(d,{title:"Port",required:"",min:1,max:65535,"model-value":i.configuration.port,"onUpdate:modelValue":e[1]||(e[1]=o=>s.updateConfiguration(o,"configuration.port"))},null,8,["model-value"])])}const V=p(b,[["render",x],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/huawei_smartlogger/device.vue"]]);export{V as default};