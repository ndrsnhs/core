import{C as r}from"./ChargePointInstallation-d3922b37.js";import{_ as i,u as a,k as p,l as s,G as d}from"./vendor-06e11d0e.js";import"./vendor-fortawesome-05d7e447.js";import"./index-3434d31b.js";import"./vendor-bootstrap-4263d7eb.js";import"./vendor-jquery-9fc083b4.js";import"./vendor-axios-22b906fb.js";import"./vendor-sortablejs-0bb60e5b.js";import"./dynamic-import-helper-be004503.js";const c={name:"ChargePointOpenwbDcAdapter",mixins:[r]},m={class:"charge-point-openwb-dc-adapter"};function u(e,o,_,l,f,g){const t=a("openwb-base-text-input");return p(),s("div",m,[d(t,{title:"IP oder Hostname",subtype:"host",required:"","model-value":e.chargePoint.configuration.ip_address,"onUpdate:modelValue":o[0]||(o[0]=n=>e.updateConfiguration(n,"configuration.ip_address"))},null,8,["model-value"])])}const B=i(c,[["render",u],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/charge_points/openwb_dc_adapter/chargePoint.vue"]]);export{B as default};