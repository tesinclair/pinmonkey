let pmAlertCounter = 0;
let pmAlerts = [];

function pm_alert(parent, { type="danger", title='Error!', message='Something went wrong. Please try again.', autoDismiss=0, dismissible=true } = {}){
    const types = ["info", "warning", "primary", "danger", "success"];
    if (!types.includes(type)){
        throw `Type must be of ${types.join(', ')}`;
    }
    if (!parent){
        throw "Parent doesn't exist";
    }

    pmAlertCounter++;
    pmAlerts.push(pmAlertCounter);

    if (pmAlertCounter > 3){
        alertToDelete = `pm-alert-${pmAlerts.shift()}`;
        document.getElementById(alertToDelete).remove();
        pmAlertCounter = 0;
    }
    
    const pmAlert = document.createElement("div");
    pmAlert.classList = `alert alert-${type} ${dismissible ? 'alert-dismissible' : ''} fade show`;
    pmAlert.id = `pm-alert-${pmAlertCounter}`;
    pmAlert.setAttribute('role', 'alert');
    pmAlert.innerHTML = `<strong>${title} </strong> ${message}`;

    if (dismissible){
        const dismissBtn = document.createElement("button");
        dismissBtn.classList = "btn-close"
        dismissBtn.setAttribute('data-bs-dismiss', 'alert');
        dismissBtn.setAttribute('aria-label', 'Close');
        pmAlert.appendChild(dismissBtn);
    }

    parent.appendChild(pmAlert);

    if (autoDismiss > 0){
        setTimeout(() => {
            pmAlert.remove();
            pmAlerts.splice(pmAlerts.indexOf(`pm-alert-${pmAlertCounter}`), 1);
        }, autoDismiss);
    }
}
