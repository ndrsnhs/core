import{E as o}from"./GeneralChargeConfig-e9bf084b.js";import{_ as a,u as n,k as s,l as c,G as l,E as p,y as f}from"./vendor-06e11d0e.js";import"./index-4e8103eb.js";import"./vendor-fortawesome-05d7e447.js";import"./vendor-bootstrap-4263d7eb.js";import"./vendor-jquery-9fc083b4.js";import"./vendor-axios-22b906fb.js";import"./vendor-sortablejs-0bb60e5b.js";import"./dynamic-import-helper-be004503.js";const d={name:"ElectricityTariffAwattar",mixins:[o]},u={class:"electricity-tariff-awattar"};function m(t,e,_,w,y,b){const i=n("openwb-base-select-input");return s(),c("div",u,[l(i,{title:"Land","not-selected":"Bitte auswählen",options:[{value:"de",text:"Deutschland"},{value:"at",text:"Österreich"}],"model-value":t.electricityTariff.configuration.country,"onUpdate:modelValue":e[0]||(e[0]=r=>t.updateConfiguration(r,"configuration.country"))},{help:p(()=>e[1]||(e[1]=[f(" Es werden die abgefragten Börsenpreise verwendet, die aWATTar bereitstellt. aWATTar-Gebühren oder Steuern werden nicht berücksichtigt. ")])),_:1},8,["model-value"])])}const $=a(d,[["render",m],["__file","/opt/openWB-dev/openwb-ui-settings/src/components/electricity_tariffs/awattar/electricity_tariff.vue"]]);export{$ as default};