import{D as r}from"./HardwareInstallation-a0083e3a.js";import{_ as p,u as o,k as d,l as c,D as n,N as m,y as l}from"./vendor-f2b8aa6f.js";import"./vendor-fortawesome-71546160.js";import"./index-b0e5e618.js";import"./vendor-bootstrap-4ad604fa.js";import"./vendor-jquery-d3cb8fad.js";import"./vendor-axios-65ecee4b.js";import"./vendor-sortablejs-2f1828d0.js";import"./dynamic-import-helper-be004503.js";const u={name:"DeviceBatterX",mixins:[r]},_={class:"device-batterx"};function f(e,t,b,v,x,g){const i=o("openwb-base-heading"),s=o("openwb-base-text-input");return d(),c("div",_,[n(i,null,{default:m(()=>[l(" Einstellungen für BatterX ")]),_:1}),n(s,{title:"IP oder Hostname",subtype:"host",required:"","model-value":e.device.configuration.ip_address,"onUpdate:modelValue":t[0]||(t[0]=a=>e.updateConfiguration(a,"configuration.ip_address"))},null,8,["model-value"])])}const y=p(u,[["render",f],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/devices/batterx/batterx/device.vue"]]);export{y as default};