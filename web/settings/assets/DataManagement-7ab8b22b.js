import{l as T,$ as O,a0 as L,a1 as z,a2 as V,a3 as H,F as A}from"./vendor-fortawesome-63a0ad05.js";import{C as j}from"./index-c0c78ae6.js";import{O as R}from"./OpenwbBackupCloudProxy-a505d168.js";import{_ as N,p as u,k as g,l as f,A as s,L as r,q as n,z as D,u as o,x as _,n as v,G as B,I as S,y as P,a2 as U}from"./vendor-20bb207d.js";import"./vendor-bootstrap-d275de6c.js";import"./vendor-jquery-89b63fca.js";import"./vendor-axios-13ef03ae.js";import"./vendor-sortablejs-ad1d2cc8.js";import"./dynamic-import-helper-be004503.js";T.add(O,L,z,V,H);const G={name:"OpenwbSystem",mixins:[j],emits:["sendCommand"],components:{FontAwesomeIcon:A,OpenwbBackupCloudProxy:R},data(){return{mqttTopicsToSubscribe:["openWB/system/configurable/backup_clouds","openWB/system/backup_cloud/config","openWB/system/device/+/component/+/config","openWB/chargepoint/+/config","openWB/vehicle/+/name","openWB/LegacySmartHome/config/get/Devices/+/device_configured","openWB/LegacySmartHome/config/get/Devices/+/device_name"],warningAcknowledged:!1,selectedRestoreFile:void 0,restoreUploadDone:!1,selectedDataMigrationFile:void 0,dataMigrationUploadDone:!1,dataMigrationConfig:[{sectionName:"Ladepunkte",sectionComponents:[{key:"cp1",label:"Ladepunkt 1",validTypes:["chargePoint"]},{key:"cp2",label:"Ladepunkt 2",validTypes:["chargePoint"]},{key:"cp3",label:"Ladepunkt 3",validTypes:["chargePoint"]},{key:"cp4",label:"Ladepunkt 4",validTypes:["chargePoint"]},{key:"cp5",label:"Ladepunkt 5",validTypes:["chargePoint"]},{key:"cp6",label:"Ladepunkt 6",validTypes:["chargePoint"]},{key:"cp7",label:"Ladepunkt 7",validTypes:["chargePoint"]},{key:"cp8",label:"Ladepunkt 8",validTypes:["chargePoint"]}]},{sectionName:"Zähler",sectionComponents:[{key:"evu",label:"EVU",validTypes:["counter"]},{key:"consumer1",label:"Verbraucher 1",validTypes:["counter"]},{key:"consumer2",label:"Verbraucher 2",validTypes:["counter"]},{key:"consumer3",label:"Verbraucher 3",validTypes:["counter"]}]},{sectionName:"Wechselrichter",sectionComponents:[{key:"pvAll",label:"Wechselrichter (Summe)",validTypes:["inverter"],help:"Die 1.9er Version von openWB speichert lediglich die Summen-Leistung aller Wechselrichter."}]},{sectionName:"Batteriespeicher",sectionComponents:[{key:"bat",label:"Speicher 1",validTypes:["battery"]}]},{sectionName:"Fahrzeuge",sectionComponents:[{key:"ev1",label:"Fahrzeug von Ladepunkt 1",validTypes:["vehicle"]},{key:"ev2",label:"Fahrzeug von Ladepunkt 2",validTypes:["vehicle"]}]},{sectionName:"SmartHome 2.0",sectionComponents:[{key:"sh1",label:"Gerät 1",validTypes:["smartHome"]},{key:"sh2",label:"Gerät 2",validTypes:["smartHome"]},{key:"sh3",label:"Gerät 3",validTypes:["smartHome"]},{key:"sh4",label:"Gerät 4",validTypes:["smartHome"]},{key:"sh5",label:"Gerät 5",validTypes:["smartHome"]},{key:"sh6",label:"Gerät 6",validTypes:["smartHome"]},{key:"sh7",label:"Gerät 7",validTypes:["smartHome"]},{key:"sh8",label:"Gerät 8",validTypes:["smartHome"]},{key:"sh9",label:"Gerät 9",validTypes:["smartHome"]},{key:"sh10",label:"Gerät 10",validTypes:["smartHome"]}]}],dataMigrationMapping:{cp1:void 0,cp2:void 0,cp3:void 0,cp4:void 0,cp5:void 0,cp6:void 0,cp7:void 0,cp8:void 0,evu:void 0,pvAll:void 0,bat:void 0,consumer1:void 0,consumer2:void 0,consumer3:void 0,sh1:void 0,sh2:void 0,sh3:void 0,sh4:void 0,sh5:void 0,sh6:void 0,sh7:void 0,sh8:void 0,sh9:void 0,sh10:void 0,ev1:void 0,ev2:void 0}}},computed:{backupCloudList(){return this.$store.state.mqtt["openWB/system/configurable/backup_clouds"]},componentConfigurations(){return this.getWildcardTopics("openWB/system/device/+/component/+/config")},chargePointOptions(){let t=this.getWildcardTopics("openWB/chargepoint/+/config");var e=[];for(const d of Object.values(t))e.push({value:d.id,text:d.name});return e},counterOptions(){var t=[];for(const e of Object.values(this.componentConfigurations))e.type=="counter"&&t.push({value:e.id,text:e.name});return t},inverterOptions(){var t=[];for(const e of Object.values(this.componentConfigurations))e.type=="inverter"&&t.push({value:e.id,text:e.name});return t},batteryOptions(){var t=[];for(const e of Object.values(this.componentConfigurations))e.type=="bat"&&t.push({value:e.id,text:e.name});return t},vehicleOptions(){let t=this.getWildcardTopics("openWB/vehicle/+/name");var e=[];for(const[d,p]of Object.entries(t)){let i=parseInt(d.match(/\/(\d\d?)\//)[1]);e.push({value:i,text:p})}return e},smartHomeOptions(){let t=this.getWildcardTopics("openWB/LegacySmartHome/config/get/Devices/+/device_configured");var e=[];for(const[d,p]of Object.entries(t))if(p==1){let i=parseInt(d.match(/\/(\d\d?)\//)[1]);e.push({value:i,text:this.$store.state.mqtt[`openWB/LegacySmartHome/config/get/Devices/${i}/device_name`]})}return e}},methods:{getBackupCloudDefaultConfiguration(t){const e=this.backupCloudList.find(d=>d.value==t);return Object.prototype.hasOwnProperty.call(e,"defaults")?{...e.defaults}:(console.warn("no default configuration found for backup cloud type!",t),{})},sendSystemCommand(t,e={}){this.$emit("sendCommand",{command:t,data:e})},getMigrationOptions(t){var e=[{value:void 0,text:"-- nicht übernehmen --"}];return t.includes("chargePoint")&&e.push(...this.chargePointOptions),t.includes("counter")&&e.push(...this.counterOptions),t.includes("inverter")&&e.push(...this.inverterOptions),t.includes("battery")&&e.push(...this.batteryOptions),t.includes("vehicle")&&e.push(...this.vehicleOptions),t.includes("smartHome")&&e.push(...this.smartHomeOptions),e},updateConfiguration(t,e){console.debug("updateConfiguration",t,e),this.updateState(t,e.value,e.object)},updateSelectedBackupCloud(t){this.updateState("openWB/system/backup_cloud/config",t,"type"),this.updateState("openWB/system/backup_cloud/config",this.getBackupCloudDefaultConfiguration(t))},updateSelectedRestoreFile(t){this.selectedRestoreFile=t.target.files[0]},updateSelectedDataMigrationFile(t){this.selectedDataMigrationFile=t.target.files[0]},uploadFile(t,e,d){return new Promise(p=>{if(e!==void 0){let i=new FormData;i.append("file",e),i.append("target",t),this.axios.post(location.protocol+"//"+location.host+"/openWB/web/settings/uploadFile.php",i,{headers:{"Content-Type":"multipart/form-data"}}).then(a=>{this.$root.postClientMessage(d,"success"),p(!0)}).catch(a=>{if(a.response){console.error(a.response.status,a.response.data);var b="Hochladen der Datei fehlgeschlagen!<br />"+a.response.status+": "+a.response.data}else a.request?(console.error(a.request),b+="Es wurde keine Antwort vom Server empfangen."):(console.error("Error",a.message),b+="Es ist ein unbekannter Fehler aufgetreten.");this.$root.postClientMessage(b,"danger"),p(!1)})}else console.error("no file selected for upload"),p(!1)})},async uploadRestoreFile(){const t="Die Sicherungsdatei wurde erfolgreich hochgeladen. Sie können die Wiederherstellung jetzt starten.";this.restoreUploadDone=await this.uploadFile("restore",this.selectedRestoreFile,t)},async uploadDataMigrationFile(){const t="Die Sicherungsdatei wurde erfolgreich hochgeladen. Sie können den Import jetzt starten.";this.dataMigrationUploadDone=await this.uploadFile("migrate",this.selectedDataMigrationFile,t)},restoreBackup(){this.sendSystemCommand("restoreBackup"),this.$store.commit("storeLocal",{name:"reloadRequired",value:!0})},dataMigration(){this.sendSystemCommand("dataMigration",this.dataMigrationMapping)}}},q={class:"system"},E=n("h2",null,"Achtung!",-1),I=n("p",null," Vor allen Aktionen auf dieser Seite ist sicherzustellen, dass kein Ladevorgang aktiv ist! Zur Sicherheit bitte zusätzlich alle Fahrzeuge von der Ladestation / den Ladestationen abstecken! ",-1),Z={key:0},K={name:"backupForm"},J=n("a",{href:"/openWB/data/backup/",target:"_blank"},"hier",-1),Q={class:"row justify-content-center"},X={class:"col-md-4 d-flex py-1 justify-content-center"},Y=n("hr",null,null,-1),$={name:"restoreForm"},ee=n("br",null,null,-1),te={class:"input-group"},ne={class:"input-group-prepend"},se={class:"input-group-text"},ie={class:"custom-file"},oe={id:"input-file-label",class:"custom-file-label",for:"input-file","data-browse":"Suchen"},ae={class:"input-group-append"},le=["disabled"],re={class:"row justify-content-center"},de={class:"col-md-4 d-flex py-1 justify-content-center"},ue=n("hr",null,null,-1),ce={name:"cloudBackupForm"},pe=n("br",null,null,-1),me=n("a",{href:"https://github.com/openWB/core/wiki/Cloud-Sicherung",target:"_blank",rel:"noopener noreferrer"}," hier ",-1),he={key:0},ge={name:"dataMigrationForm"},fe=n("br",null,null,-1),be=n("br",null,null,-1),ke={class:"input-group"},ye={class:"input-group-prepend"},_e={class:"input-group-text"},ve={class:"custom-file"},we={id:"data-migration-file-label",class:"custom-file-label",for:"data-migration-file","data-browse":"Suchen"},Ce={class:"input-group-append"},De=["disabled"],Be={class:"row justify-content-center"},Se={class:"col-md-4 d-flex py-1 justify-content-center"},Fe={name:"resetForm"},We={class:"row justify-content-center"},Me={class:"col-md-4 d-flex py-1 justify-content-center"};function xe(t,e,d,p,i,a){const b=u("openwb-base-button-group-input"),m=u("openwb-base-alert"),k=u("openwb-base-heading"),c=u("font-awesome-icon"),y=u("openwb-base-click-button"),C=u("openwb-base-select-input"),F=u("openwb-base-button-input"),W=u("openwb-backup-cloud-proxy"),M=u("openwb-base-submit-buttons"),w=u("openwb-base-card");return g(),f("div",q,[s(m,{subtype:"danger"},{default:r(()=>[E,I,s(b,{title:"Ich habe die Warnung verstanden",buttons:[{buttonValue:!1,text:"Nein",class:"btn-outline-danger"},{buttonValue:!0,text:"Ja",class:"btn-outline-success"}],modelValue:this.warningAcknowledged,"onUpdate:modelValue":e[0]||(e[0]=l=>this.warningAcknowledged=l)},null,8,["modelValue"])]),_:1}),i.warningAcknowledged?(g(),f("div",Z,[s(w,{title:"Sicherung / Wiederherstellung",subtype:"success",collapsible:!0,collapsed:!0},{default:r(()=>[n("form",K,[s(k,null,{default:r(()=>[o("Sicherung")]),_:1}),s(m,{subtype:"danger"},{default:r(()=>[o(' Aktuell können nur Sicherungen wiederhergestellt werden, die in den Entwicklungszweigen "master", "Beta" oder "Release" erstellt wurden! ')]),_:1}),s(m,{subtype:"info"},{default:r(()=>[o(" Nachdem die Sicherung abgeschlossen ist, kann die erstellte Datei über den Link in der Benachrichtigung oder "),J,o(" heruntergeladen werden. ")]),_:1}),n("div",Q,[n("div",X,[s(y,{class:"btn-success clickable",onButtonClicked:e[1]||(e[1]=l=>a.sendSystemCommand("createBackup",{use_extended_filename:!0}))},{default:r(()=>[o(" Sicherung erstellen "),s(c,{"fixed-width":"",icon:["fas","archive"]})]),_:1})])])]),Y,n("form",$,[s(k,null,{default:r(()=>[o("Wiederherstellung")]),_:1}),s(m,{subtype:"danger"},{default:r(()=>[o(" Für die Wiederherstellung wird eine aktive Internetverbindung benötigt."),ee,o(' Aktuell können nur Sicherungen wiederhergestellt werden, die in den Entwicklungszweigen "master", "Beta" oder "Release" erstellt wurden! ')]),_:1}),n("div",te,[n("div",ne,[n("div",se,[s(c,{"fixed-width":"",icon:["fas","file-archive"]})])]),n("div",ie,[n("input",{id:"input-file",type:"file",class:"custom-file-input",accept:".tar.gz,application/gzip,application/tar+gzip",onChange:e[2]||(e[2]=l=>a.updateSelectedRestoreFile(l))},null,32),n("label",oe,_(i.selectedRestoreFile?i.selectedRestoreFile.name:"Bitte eine Datei auswählen"),1)]),n("div",ae,[n("button",{class:v(["btn",i.selectedRestoreFile?"btn-success clickable":"btn-outline-success"]),disabled:!i.selectedRestoreFile,type:"button",onClick:e[3]||(e[3]=l=>a.uploadRestoreFile())},[o(" Hochladen "),s(c,{"fixed-width":"",icon:["fas","upload"]})],10,le)])]),n("div",re,[n("div",de,[s(y,{class:v(i.restoreUploadDone?"btn-success clickable":"btn-outline-success"),disabled:!i.restoreUploadDone,onButtonClicked:e[4]||(e[4]=l=>a.restoreBackup())},{default:r(()=>[o(" Wiederherstellung starten "),s(c,{"fixed-width":"",icon:["fas","box-open"]})]),_:1},8,["class","disabled"])])])]),ue,n("form",ce,[s(k,null,{default:r(()=>[o(" Automatische Sicherung in einen Cloud-Dienst ")]),_:1}),s(m,{subtype:"info"},{default:r(()=>[o(" Zwischen Mitternacht und 5:00 Uhr wird automatisch eine Sicherung erstellt und in den angegebenen Cloud-Dienst (nicht openWB Cloud!) hochgeladen. Ist kein Cloud-Dienst konfiguriert, wird keine automatische Sicherung erstellt. Die automatische Sicherung kann unabhängig von der openWB Cloud genutzt werden."),pe,o(" Die Anleitung zur Konfiguration des Cloud-Dienstes findest Du "),me,o(" . ")]),_:1}),s(C,{class:"mb-2",title:"Backup-Cloud",options:a.backupCloudList,"model-value":t.$store.state.mqtt["openWB/system/backup_cloud/config"].type,"onUpdate:modelValue":e[5]||(e[5]=l=>a.updateSelectedBackupCloud(l))},null,8,["options","model-value"]),t.$store.state.mqtt["openWB/system/backup_cloud/config"].type?(g(),f("div",he,[s(F,{title:"Manuelle Cloud-Sicherung",buttonText:"Sicherung erstellen und hochladen",subtype:"success",onButtonClicked:e[6]||(e[6]=l=>a.sendSystemCommand("createCloudBackup",{}))}),s(W,{backupCloudType:t.$store.state.mqtt["openWB/system/backup_cloud/config"].type,configuration:t.$store.state.mqtt["openWB/system/backup_cloud/config"].configuration,"onUpdate:configuration":e[7]||(e[7]=l=>a.updateConfiguration("openWB/system/backup_cloud/config",l))},null,8,["backupCloudType","configuration"])])):D("v-if",!0),s(M,{formName:"cloudBackupForm",hideReset:!0,hideDefaults:!0,onSave:e[8]||(e[8]=l=>t.$emit("save")),onReset:e[9]||(e[9]=l=>t.$emit("reset")),onDefaults:e[10]||(e[10]=l=>t.$emit("defaults"))})])]),_:1}),s(w,{title:"Datenübernahme",subtype:"success",collapsible:!0,collapsed:!0},{default:r(()=>[n("form",ge,[s(m,{subtype:"info"},{default:r(()=>[o(" Hier kann die Sicherung einer älteren 1.9er Version hochgeladen werden, um vorhandene historische Daten (Diagramme und Ladeprotokolle) sowie Cloud-Daten und Seriennummer in diese Installation zu importieren. Die Zuordnung zwischen den alten und neuen Komponenten muss manuell durchgeführt werden."),fe,o(" Die Portierung kann einige Minuten dauern. Du erhältst eine Meldung, wenn die Datenübernahme abgeschlossen ist. ")]),_:1}),s(m,{subtype:"danger"},{default:r(()=>[o(" Vor der Datenübernahme unbedingt eine Sicherung erstellen."),be,o(" Die Datenübernahme kann nur durch Einspielen einer Sicherung rückgängig gemacht werden! ")]),_:1}),n("div",ke,[n("div",ye,[n("div",_e,[s(c,{"fixed-width":"",icon:["fas","file-archive"]})])]),n("div",ve,[n("input",{id:"data-migration-file",type:"file",class:"custom-file-input",accept:".tar.gz,application/gzip,application/tar+gzip",onChange:e[11]||(e[11]=l=>a.updateSelectedDataMigrationFile(l))},null,32),n("label",we,_(i.selectedDataMigrationFile?i.selectedDataMigrationFile.name:"Bitte eine Datei auswählen"),1)]),n("div",Ce,[n("button",{class:v(["btn",i.selectedDataMigrationFile?"btn-success clickable":"btn-outline-success"]),disabled:!i.selectedDataMigrationFile,type:"button",onClick:e[12]||(e[12]=l=>a.uploadDataMigrationFile())},[o(" Hochladen "),s(c,{"fixed-width":"",icon:["fas","upload"]})],10,De)])]),s(k,null,{default:r(()=>[o("Zuordnung der Komponenten")]),_:1}),(g(!0),f(B,null,S(i.dataMigrationConfig,l=>(g(),f("div",{key:l.sectionName},[s(k,null,{default:r(()=>[o(_(l.sectionName),1)]),_:2},1024),(g(!0),f(B,null,S(l.sectionComponents,h=>(g(),P(C,{key:h.key,title:h.label,options:a.getMigrationOptions(h.validTypes),modelValue:i.dataMigrationMapping[h.key],"onUpdate:modelValue":x=>i.dataMigrationMapping[h.key]=x},U({_:2},[h.help?{name:"help",fn:r(()=>[o(_(h.help),1)]),key:"0"}:void 0]),1032,["title","options","modelValue","onUpdate:modelValue"]))),128))]))),128)),n("div",Be,[n("div",Se,[s(y,{class:v(i.dataMigrationUploadDone?"btn-success clickable":"btn-outline-success"),disabled:!i.dataMigrationUploadDone,onButtonClicked:e[13]||(e[13]=l=>a.dataMigration())},{default:r(()=>[o(" Datenübernahme starten "),s(c,{"fixed-width":"",icon:["fas","box-open"]})]),_:1},8,["class","disabled"])])])])]),_:1}),n("form",Fe,[s(w,{title:"Zurücksetzen",subtype:"danger",collapsible:!0,collapsed:!0},{footer:r(()=>[n("div",We,[n("div",Me,[s(y,{class:"btn-danger clickable",onButtonClicked:e[14]||(e[14]=l=>a.sendSystemCommand("factoryReset",{}))},{default:r(()=>[s(c,{"fixed-width":"",icon:["fas","skull-crossbones"]}),o(" Zurücksetzen "),s(c,{"fixed-width":"",icon:["fas","skull-crossbones"]})]),_:1})])])]),default:r(()=>[s(m,{subtype:"danger"},{default:r(()=>[o(" Alle Einstellungen, angelegte Geräte/Komponenten, Ladepunkte und Fahrzeuge, etc, Tages-, Monats- und Jahresauswertungen sowie das Ladeprotokoll werden unwiederbringlich gelöscht. Auch die Vorkonfiguration im Auslieferungszustand wird gelöscht. Die openWB muss danach komplett neu eingerichtet werden. Die openWB wird hierfür automatisch neu gestartet. Bitte erstelle vor dem Zurücksetzen eine Sicherung! ")]),_:1})]),_:1})])])):D("v-if",!0)])}const Ne=N(G,[["render",xe],["__file","/opt/openWB-dev/openwb-ui-settings/src/views/DataManagement.vue"]]);export{Ne as default};