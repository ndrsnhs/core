import{_ as p,q as t,k as l,l as c,B as a,M as m,x as _,u as f,y as b}from"./vendor-f0f38b48.js";import"./vendor-sortablejs-cbf37f8f.js";const g={name:"DeviceOpenwbFlex",emits:["update:configuration"],props:{configuration:{type:Object,required:!0},componentId:{required:!0}},methods:{updateConfiguration(n,e=void 0){this.$emit("update:configuration",{value:n,object:e})}}},v={class:"device-openwb-flex"},x={class:"small"};function w(n,e,i,B,h,s){const u=t("openwb-base-heading"),r=t("openwb-base-text-input"),d=t("openwb-base-number-input");return l(),c("div",v,[a(u,null,{default:m(()=>[_(" Einstellungen für openWB-Flex "),f("span",x,"(Modul: "+b(n.$options.name)+")",1)]),_:1}),a(r,{title:"IP oder Hostname",subtype:"host",required:"","model-value":i.configuration.ip_address,"onUpdate:modelValue":e[0]||(e[0]=o=>s.updateConfiguration(o,"configuration.ip_address"))},null,8,["model-value"]),a(d,{title:"Port",required:"",min:1,max:65535,"model-value":i.configuration.port,"onUpdate:modelValue":e[1]||(e[1]=o=>s.updateConfiguration(o,"configuration.port"))},null,8,["model-value"])])}const V=p(g,[["render",w],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/openwb_flex/device.vue"]]);export{V as default};