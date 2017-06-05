/* ------------------------------------------------------------------------------------------------------------- Test Data */

/*
    Acra errors Data Layout:
    {
        offset: ?
        rows:[
            {
                id: random
                key: date, or version and date
                value: {
                    android_version:
                    application_version_name: ex 2.17, 2.18.beta
                    device:
                    installation_id: ?
                    signature: {
                        digest: ex "io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 1404 | account: erika | 400 :  at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)"
                        full: 
                        rootCause: ex "java.lang.Exception at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:211)"
                    }
                    user_crash_date:
                }
            }
        ]
        total_rows:
    }
*/

// USAGE: localhost:3000/?type=[all,version]&typeval=['',2.17]&limit=[1000]





var typeInSearch = 'all'; //             all or version
var typeValueInSearch = '';
var limitInSearch = '5000';


/* --------------------------------------------------------------------------------------------------------------- Imports */
var http = require("http");
var express = require('express');
var request = require('sync-request');

var app = express();

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
});


/* --------------------------------------------------------------------------------------------------------------- Main */
app.get('/', function (req, res) {

    logMainTask("Downloading acra report");
    var type = getAcraURLParam(req.query.type, typeInSearch);
    var typeValue = getAcraURLParam(req.query.typeval, typeValueInSearch);
    var limit = getAcraURLParam(req.query.limit, limitInSearch);

    var acraResponse = getAcraData(
        getAcraURL(type, typeValue, limit),
        function(acraRes){
            var body = '';

            acraRes.on('data', function(chunk){
                body += chunk;
            });

            acraRes.on('end', function(){            
                logSubtask("Acra report downloaded!");

                var acraResponse = JSON.parse(body);

                var errors = acraResponse.rows;
                if(errors){
                    logSubtask("Number of Errors: " + errors.length);
                    logSubtask("acraResponse.rows: " + errors[0].version);
                    // console.log("Grouping and filtering items by RootCause, and ranking by occurences");
                    // groupItemsByRootCause(acraResponse);

                    //errors = filterItemsByFarm(errors);

                    errors = filterErrorsByAccount(errors);

                    errors = filterItemsByRootCause(errors);
                    console.log("Errors filtered by Root Cause:");
                    console.log("Total: ", errors.length);

                    //logErrorsArray(errors);

                    errors = groupByRootCause(errors);
                    //logErrorsGroupedByRootCause(errors);

                    errors = getSortedArrayByRootCauseOccurence(errors);
                    logRootCausesSortedByOccurence(res, errors);
                }
            });
    });

});

/* --------------------------------------------------------------------------------------------------------------- Get Acra Data */
function getAcraData(url, callback){
    http
        .get(url, callback)
        .on('error', onGetDataError);
}

function getAcraURL(type, typeValue, limit){
    var url = (function(){
        var all = function(version, limit){
            logSubtask("Fetching errors for all versions. Limit of items: " + limit);
            return 'http://acra.strider.io/acra-strider/_design/acra-storage/_view/recent-items?descending=true&include_docs=false&limit='+limit;
        };
        var byVersion = function(version, limit){
            logSubtask("Fetching errors for version " + version + ". Limit of items: " + limit);
            return 'http://acra.strider.io/acra-strider/_design/acra-storage/_view/recent-items-by-appver?descending=true&endkey=%5B'+version+'%5D&include_docs=false&limit='+limit+'&reduce=false&startkey=%5B'+version+',%7B%7D%5D';
        }

        return{
            all: all,
            version: byVersion
        };
    })();

    return url[type](typeValue, limit);
}

function getAcraURLParam(param, defaultVal){
    if(!param){
        return defaultVal;
    }
    return param;
}

function onGetDataError(error){
    console.error("Got an error: ", error);
}

function getTestData(){
    return {
        "total_rows":24836,
        "offset":23090,
        "rows":[
            {"id":"929d20a3-7cfa-4baf-84b8-dd79f52db3ec","key":[2.17,"2016-12-22T12:06:16.558Z"],"value":{"user_crash_date":"2016-12-22T12:06:16.558Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.ConnectException: failed to connect to v2.strider.io/198.20.66.226 (port 80): connect failed: ETIMEDOUT (Connection timed out) | farm: 1335 | account: cdiel | 0 at io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.ConnectException: failed to connect to v2.strider.io/198.20.66.226 (port 80): connect failed: ETIMEDOUT (Connection timed out) | farm: 1335 | account: cdiel | 0 : \tat io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","rootCause":"libcore.io.ErrnoException: connect failed: ETIMEDOUT (Connection timed out) \tat libcore.io.Posix.connect(Native Method)"},"installation_id":"91c33937-b71d-4cda-b183-9de781ee8cef","device":"samsung samsung SM-T113NU"}},
            {"id":"84a0d75a-11cf-4d59-a1dd-f5e8b3383139","key":[2.17,"2016-12-22T12:04:06.644Z"],"value":{"user_crash_date":"2016-12-22T12:04:06.644Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: error sending upgrades info data  | farm: 0 | account: douglasr | 0 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.getUpgradesInfo(ScoutWSClient.java:436)","digest":"io.strider.core.business.exception.StriderHTTPException: error sending upgrades info data  | farm: 0 | account: douglasr | 0 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.getUpgradesInfo(ScoutWSClient.java:436)","rootCause":"libcore.io.GaiException: getaddrinfo failed: EAI_NODATA (No address associated with hostname) at io.strider.mobile.module.scout.business.ws.ScoutWSClient.getUpgradesInfo(ScoutWSClient.java:414)"},"installation_id":"18cca246-dfea-4ca9-9eb0-b899af4e75e7","device":"samsung samsung SM-T113NU"}},
            {"id":"8668c4ec-4b5a-46fa-8474-fac789f439e2","key":[2.17,"2016-12-22T10:49:26.108Z"],"value":{"user_crash_date":"2016-12-22T10:49:26.108Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderException: java.lang.RuntimeException: An error occured while executing doInBackground() | farm: 1335 | account: cdiel at io.strider.mobile.delegate.ServiceDelegate$1.uncaughtException(ServiceDelegate.java:167)","digest":"io.strider.core.business.exception.StriderException: java.lang.RuntimeException: An error occured while executing doInBackground() | farm: 1335 | account: cdiel : \tat io.strider.mobile.delegate.ServiceDelegate$1.uncaughtException(ServiceDelegate.java:167)","rootCause":"android.view.ViewRootImpl$CalledFromWrongThreadException: Only the original thread that created a view hierarchy can touch its views. at io.strider.mobile.module.scout.activity.fragment.CollectionMasterFragment.clearSync(CollectionMasterFragment.java:426)"},"installation_id":"91c33937-b71d-4cda-b183-9de781ee8cef","device":"samsung samsung SM-T113NU"}},
            {"id":"19e9dca4-16f3-42c8-930c-f82dc93860f2","key":[2.17,"2016-12-22T10:30:26.003Z"],"value":{"user_crash_date":"2016-12-22T10:30:26.003Z","android_version":"4.4.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data \"Longitude should be between -180 and 180\" | farm: 1111 | account: thais | 400 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","digest":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data \"Longitude should be between -180 and 180\" | farm: 1111 | account: thais | 400 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","rootCause":"java.lang.Exception at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:211)"},"installation_id":"fe5ca1aa-18f0-4d99-acc1-c9fc721170cf","device":"samsung samsung SM-G900F"}},
            {"id":"2baa8818-9bcd-46cc-b25f-7a9d1f4c41b9","key":[2.17,"2016-12-22T08:19:42.122Z"],"value":{"user_crash_date":"2016-12-22T08:19:42.122Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderException: java.lang.NumberFormatException: Invalid int: \"\u4efc\uff4e\u00fb\uff00\u4efc\" | farm: 914 | account: luisfnascimento at io.strider.mobile.delegate.ServiceDelegate$1.uncaughtException(ServiceDelegate.java:167)","digest":"io.strider.core.business.exception.StriderException: java.lang.NumberFormatException: Invalid int: \"\u4efc\uff4e\u00fb\uff00\u4efc\" | farm: 914 | account: luisfnascimento : \tat io.strider.mobile.delegate.ServiceDelegate$1.uncaughtException(ServiceDelegate.java:167)","rootCause":"java.lang.NumberFormatException: Invalid int: \"\u4efc\uff4e\u00fb\uff00\u4efc\" at io.strider.mobile.map.MapController.paintTaskAreas(MapController.java:96)"},"installation_id":"7abf94b9-efa6-4aff-b8a4-62215e31c2d6","device":"samsung samsung SM-T110"}},
            {"id":"c0ce165e-cd7f-4ac9-b543-a20c1fe2b2f4","key":[2.17,"2016-12-22T08:19:41.154Z"],"value":{"user_crash_date":"2016-12-22T08:19:41.154Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderException: java.lang.NullPointerException | farm: 914 | account: luisfnascimento at io.strider.mobile.delegate.ServiceDelegate$1.uncaughtException(ServiceDelegate.java:167)","digest":"io.strider.core.business.exception.StriderException: java.lang.NullPointerException | farm: 914 | account: luisfnascimento : \tat io.strider.mobile.delegate.ServiceDelegate$1.uncaughtException(ServiceDelegate.java:167)","rootCause":"java.lang.NullPointerException \tat io.strider.map.wrapper.android.MapImageWrapper.getHeight(MapImageWrapper.java:36)"},"installation_id":"7abf94b9-efa6-4aff-b8a4-62215e31c2d6","device":"samsung samsung SM-T110"}},
            {"id":"1af92a0d-12dc-4fc1-9c8f-802ce56d4c3f","key":[2.17,"2016-12-22T08:19:40.028Z"],"value":{"user_crash_date":"2016-12-22T08:19:40.028Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 910 | account: luisfnascimento | 0 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","digest":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 910 | account: luisfnascimento | 0 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","rootCause":"java.net.UnknownHostException: Unable to resolve host \"v2.strider.io\": No address associated with hostname at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:197)"},"installation_id":"7abf94b9-efa6-4aff-b8a4-62215e31c2d6","device":"samsung samsung SM-T110"}},
            {"id":"6d25671e-4464-40b4-be8d-c3e18a038f58","key":[2.17,"2016-12-22T08:19:38.886Z"],"value":{"user_crash_date":"2016-12-22T08:19:38.886Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 910 | account: luisfnascimento | 0 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","digest":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 910 | account: luisfnascimento | 0 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","rootCause":"java.net.UnknownHostException: Unable to resolve host \"v2.strider.io\": No address associated with hostname at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:197)"},"installation_id":"7abf94b9-efa6-4aff-b8a4-62215e31c2d6","device":"samsung samsung SM-T110"}},
            {"id":"eba94487-b04e-45a8-bf54-267535da516d","key":[2.17,"2016-12-22T08:19:37.742Z"],"value":{"user_crash_date":"2016-12-22T08:19:37.742Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 910 | account: luisfnascimento | 0 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","digest":"io.strider.core.business.exception.StriderHTTPException: error sending tracker log data  | farm: 910 | account: luisfnascimento | 0 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:215)","rootCause":"libcore.io.ErrnoException: recvfrom failed: ETIMEDOUT (Connection timed out) at io.strider.mobile.module.scout.business.ws.ScoutWSClient.sendTrackerLog(ScoutWSClient.java:197)"},"installation_id":"7abf94b9-efa6-4aff-b8a4-62215e31c2d6","device":"samsung samsung SM-T110"}},
            {"id":"a30a81fe-f489-4a4d-b6a3-86c467a1a350","key":[2.17,"2016-12-22T07:36:40.490Z"],"value":{"user_crash_date":"2016-12-22T07:36:40.490Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketTimeoutException | farm: 1481 | account: vitor.a | 200 at io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketTimeoutException | farm: 1481 | account: vitor.a | 200 : \tat io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","rootCause":"java.net.SocketTimeoutException \tat java.net.PlainSocketImpl.read(PlainSocketImpl.java:491)"},"installation_id":"1e94cc1a-cb73-4bc4-bd77-add956ec1c96","device":"samsung samsung SM-T113NU"}},
            {"id":"6c84fbfe-7112-4224-8a2b-f7553cd9044e","key":[2.17,"2016-12-22T00:54:39.768Z"],"value":{"user_crash_date":"2016-12-22T00:54:39.768Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketTimeoutException | farm: 1463 | account: vitor.a | 200 at io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketTimeoutException | farm: 1463 | account: vitor.a | 200 : \tat io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","rootCause":"java.net.SocketTimeoutException \tat java.net.PlainSocketImpl.read(PlainSocketImpl.java:491)"},"installation_id":"1e94cc1a-cb73-4bc4-bd77-add956ec1c96","device":"samsung samsung SM-T113NU"}},
            {"id":"fe5d81bc-adbf-485b-a9c1-7b3fb60ddca8","key":[2.17,"2016-12-22T00:11:13.770Z"],"value":{"user_crash_date":"2016-12-22T00:11:13.770Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.ProtocolException: unexpected end of stream | farm: 1421 | account: ricardon | 200 at io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.ProtocolException: unexpected end of stream | farm: 1421 | account: ricardon | 200 : \tat io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","rootCause":"java.net.ProtocolException: unexpected end of stream \tat com.android.okhttp.internal.http.HttpTransport$FixedLengthInputStream.read(HttpTransport.java:389)"},"installation_id":"1bc199af-325e-44d4-a584-ead372ab341f","device":"samsung samsung SM-T113NU"}},
            {"id":"c7eab96c-b481-4da9-a840-17124e17d850","key":[2.17,"2016-12-21T21:37:44.055Z"],"value":{"user_crash_date":"2016-12-21T21:37:44.055Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.UnknownHostException: Unable to resolve host \"v2.strider.io\": No address associated with hostname | farm: 0 | account: helielton | 0 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.downloadStriderApkToFile(ScoutWSClient.java:800)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.UnknownHostException: Unable to resolve host \"v2.strider.io\": No address associated with hostname | farm: 0 | account: helielton | 0 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.downloadStriderApkToFile(ScoutWSClient.java:800)","rootCause":"libcore.io.GaiException: getaddrinfo failed: EAI_NODATA (No address associated with hostname) at io.strider.mobile.module.scout.business.ws.ScoutWSClient.downloadStriderApkToFile(ScoutWSClient.java:768)"},"installation_id":"28784dad-5669-4c14-b513-6f1719aa4e23","device":"samsung samsung SM-T113NU"}},
            {"id":"793ef6a8-1dcd-47a9-a3bd-a49f70ebbfdc","key":[2.17,"2016-12-21T21:37:41.510Z"],"value":{"user_crash_date":"2016-12-21T21:37:41.510Z","android_version":"4.4.4","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: error sending upgrades info data  | farm: 0 | account: helielton | 0 at io.strider.mobile.module.scout.business.ws.ScoutWSClient.getUpgradesInfo(ScoutWSClient.java:436)","digest":"io.strider.core.business.exception.StriderHTTPException: error sending upgrades info data  | farm: 0 | account: helielton | 0 : \tat io.strider.mobile.module.scout.business.ws.ScoutWSClient.getUpgradesInfo(ScoutWSClient.java:436)","rootCause":"libcore.io.GaiException: getaddrinfo failed: EAI_NODATA (No address associated with hostname) at io.strider.mobile.module.scout.business.ws.ScoutWSClient.getUpgradesInfo(ScoutWSClient.java:414)"},"installation_id":"28784dad-5669-4c14-b513-6f1719aa4e23","device":"samsung samsung SM-T113NU"}},
            {"id":"2ab387a9-87bc-4278-b4fe-f553dc1509b9","key":[2.17,"2016-12-21T21:31:56.136Z"],"value":{"user_crash_date":"2016-12-21T21:31:56.136Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketTimeoutException | farm: 1344 | account: alan | 200 at io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketTimeoutException | farm: 1344 | account: alan | 200 : \tat io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","rootCause":"java.net.SocketTimeoutException \tat java.net.PlainSocketImpl.read(PlainSocketImpl.java:491)"},"installation_id":"308b2016-d898-4706-a65b-dc6966aeff24","device":"samsung samsung SM-T110"}},
            {"id":"0b99a980-2296-4362-a197-5e9293454307","key":[2.17,"2016-12-21T21:31:42.593Z"],"value":{"user_crash_date":"2016-12-21T21:31:42.593Z","android_version":"4.2.2","application_version_name":2.17,"signature":{"full":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketException: recvfrom failed: ETIMEDOUT (Connection timed out) | farm: 1344 | account: alan | 200 at io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","digest":"io.strider.core.business.exception.StriderHTTPException: java.net.SocketException: recvfrom failed: ETIMEDOUT (Connection timed out) | farm: 1344 | account: alan | 200 : \tat io.strider.core.business.ws.WSClient.downloadFarmBundleToFile(WSClient.java:257)","rootCause":"libcore.io.ErrnoException: recvfrom failed: ETIMEDOUT (Connection timed out) \tat libcore.io.Posix.recvfromBytes(Native Method)"},"installation_id":"308b2016-d898-4706-a65b-dc6966aeff24","device":"samsung samsung SM-T110"}}
        ]
    };
}

function getErrorCompleteData(errorKey){
    var res = request('GET','http://acra.strider.io/acra-strider/' + errorKey);
    var data = res.body.toString('utf-8');
    return JSON.parse(data).STACK_TRACE;
}

/* --------------------------------------------------------------------------------------------------------------- Filter functions */
function containTagsFilter(error){
    function checkTag(tag){
        var valid = false;
        if(errorHasDigest){
            valid = (getErrorDigest(error).indexOf(tag) != -1);
        }
        return valid;
    }
    var contains = this.some(checkTag);

    return contains;
}

function doesNotContainTagsFilter(error){
    function checkTag(tag){
        var valid = true;
        if(errorHasRootCause(error)){
            valid = (getErrorRootCause(error).indexOf(tag) == -1);
        }
        if(valid && errorHasDigest(error)){
            valid = (getErrorDigest(error).indexOf(tag) == -1);
        }
        return valid;
    }
    var contains = this.every(checkTag);

    return contains;
}

function filterErrorsByContainTags(errors, tags, filterDescription){
    var errorsFiltered = errors.filter(containTagsFilter, tags);

    logSubtask('Errors filtered by ' + filterDescription + ' - Total: ' + errorsFiltered.length);

    return errorsFiltered;    
}

function getIdsFilterFormatted(idsList, prefix, suffix){
    var idFilter = [];
    idsList.forEach(function(id){
        idFilter.push(prefix + id + suffix);
    });

    return idFilter;
}

/* --------------------------------------------------------------------------------------------------------------- Filter by Account */
function filterErrorsByAccount(errors){
    logMainTask("Filtering results by account.");
    var accountIdsToFilter = getAccountIdsToFilter();

    var accountIdFilter = getAccountIdFilter(accountIdsToFilter);

    return filterErrorsByContainTags(errors, accountIdFilter, 'Account');
}

function getAccountIdFilter(accountIdsList){
    return getIdsFilterFormatted(accountIdsList, 'account: ', '');
}

function getAccountIdsToFilter(){
    var idsToFilter = [
        'tyler',
    ];

    logSubtask("Account Ids to filter: " + idsToFilter.join(', '));

    return idsToFilter;
}


/* --------------------------------------------------------------------------------------------------------------- Filter by farm */
function filterItemsByFarm(errors){
    logMainTask("Filtering results by farm.");

    var farmIdsToFilter = getFarmIdsToFilter();

    var farmIdFilter = getFarmIdFilter(farmIdsToFilter);

    return filterErrorsByContainTags(errors, farmIdFilter, 'Farm');
}

function getFarmIdFilter(farmIdsList){
    return getIdsFilterFormatted(farmIdsList, 'farm: ', '');
}

function getFarmIdsToFilter(){
    var farmIdsToFilter = {
        fogliatelli: [
            '996'
        ],
        zilor: [
            '910',
            '911',
            '912',
            '913',
            '914',
            '1099',
            '1100',
            '1101',
            '1102',
            '1103',
            '1104',
            '1105',
            '1106',
            '1107',
            '1108'
        ]
    };

    logSubtask("Farm Ids to filter: " + farmIdsToFilter.fogliatelli.join(', '));

    return farmIdsToFilter.fogliatelli;
}

/* --------------------------------------------------------------------------------------------------------------- Filter by rootCause */
function filterItemsByRootCause(errors){
    console.log("Filtering results by root cause.");

    var errorsToRemoveFilter = getErrorsToRemoveFilter();

    var errorsFiltered = errors.filter(doesNotContainTagsFilter, errorsToRemoveFilter);

    return errorsFiltered;
}

function getErrorsToRemoveFilter(){
    return [
        "ETIMEDOUT",
        "EHOSTUNREACH",
        "ECONNRESET",
        "ENETUNREACH",
        "EAI_NODATA",
        "ECONNREFUSED",

        "SocketTimeoutException",
        "ConnectTimeoutException",
        "UnknownHostException",
        "HttpResponseException",
        "HttpResponseException",
        "StriderHTTPException"
    ];
}

/* --------------------------------------------------------------------------------------------------------------- Group by rootCause */
function groupByRootCause(errors){
    var errorsGrouped = errors.reduce(function(errorsObj, error){
        var rootCause = "ROOT CAUSE NOT PRESENT";
        if(errorHasRootCause(error)){
            rootCause = getErrorRootCause(error);
        }

        if(!errorsObj.hasOwnProperty(rootCause)){
            errorsObj[rootCause] = [];
        }

        errorsObj[rootCause].push(error);

        return errorsObj;

    }, {});

    return errorsGrouped;
}

function getSortedArrayByRootCauseOccurence(errorsGroupedByRootCause){
    var rootCauseArray = [];
    for(var rootCause in errorsGroupedByRootCause){
        rootCauseArray.push({
            'rootCause': rootCause,
            'occurences': errorsGroupedByRootCause[rootCause].length,
            'lastOccurence': getErrorsLastOccurence(errorsGroupedByRootCause[rootCause]),
            stackTrace: getErrorCompleteData(errorsGroupedByRootCause[rootCause][0].id),
			'application_version_name': getErrorValueProperty(errorsGroupedByRootCause[rootCause][0], 'application_version_name')
        });
    };

    rootCauseArray.sort(function(itemA, itemB){
        return itemA.occurences = itemB.occurences;
    });

    return rootCauseArray;
}

function getErrorsLastOccurence(errors){
    errors.sort(function(errorA, errorB){
        var sortValue = 0;
        if(errorHasDate(errorA)){
            sortValue = -1;
            if(errorHasDate(errorB)){
                var dateA = (new Date(getErrorDate(errorA))).valueOf();
                var dateB = (new Date(getErrorDate(errorB))).valueOf();
                sortValue = dateB - dateA;
            }
        }
        else if(errorHasDate(errorB)){
            sortValue = 1;
            
        }
        return sortValue;
    });

    var lastOccurence = (new Date(getErrorDate(errors[0]))).toString();
    
    return lastOccurence;
}

/* --------------------------------------------------------------------------------------------------------------- Log Errors */
function logErrorsArray(errors){
    console.log("\n == Listing the Errors == \n");
    errors.forEach(function(error){
        console.log(getErrorLog(error));
    });

    function getErrorLog(error){
        var errorLog = "";

        if(errorHasDate(error)){
            errorLog += "Date: " + getErrorDate(error) + "\n";            
        }
        if(errorHasRootCause(error)){
            errorLog += "Root Cause: " + getErrorRootCause(error) + "\n";
        }

        errorLog += "\n";

        return errorLog;
    }
}

function logErrorsGroupedByRootCause(errors){
    console.log("\n == Listing the Errors Grouped by Root Cause == \n");

    for(var rootCause in errors){
        console.log(rootCause + ' - Occurences: ' + errors[rootCause].length + '\n');
    }
}

function logRootCausesSortedByOccurence(res,rootCauses){
    
    var html = "<html><body>";
    html += "\n == Listing the Root Causes Sorted by Occurences == \n";

    html += '<table border="1">';
    html += "<tr>";
    html += '<th>Root Cause</th>';   
    html += '<th>Occurences</th>';   
    html += '<th>Last Occurence</th>';   
    html += '<th>Versão</th>';   
    html += "</tr>";
    rootCauses.forEach(function(item){
		
        html += '<tr>';
        html += '<td><strong>'+ item.rootCause + '</strong></td>';   
        html += '<td>'+ item.occurences + '</td>';     
        html += '<td>'+ item.lastOccurence + '</td>';   
        html += '<td>'+ item.application_version_name + '</td>';   
        html += '</tr>'
       
        html += '<tr>';
		
        html += '<td colspan="4">'
        /*
        for( var i in item.stackTrace){

             html += '<br/>' + item.stackTrace[i];

        }*/
        
        html += '</td>';
		
        html += '</tr>';

    });
    html += "</table>";

     html += "</body></html>";

     res.send(html);
}

function logMainTask(logText){
    console.log('\n\n == ' + logText + ' == \n');
}

function logSubtask(logText){
    console.log('--- ' + logText);
}

/* --------------------------------------------------------------------------------------------------------------- Data Manipulation Helpers */
function getErrorRootCause(error){
    return getErrorSignatureProperty(error, 'rootCause');
}

function getErrorDigest(error){
    return getErrorSignatureProperty(error, 'digest');
}

function getErrorDate(error){
    var errorDateString = getErrorValueProperty(error, 'user_crash_date');
    var errorDate = new Date(errorDateString);
    return errorDate.toString();
}

function getErrorSignatureProperty(error, propertyName){
    var signature = getErrorValueProperty(error, 'signature');
    return signature[propertyName];
}

function getErrorValueProperty(error, propertyName){
    return error.value[propertyName];
}

function errorHasDigest(error){
    return isErrorSignaturePropertyPresent(error, 'digest');
}

function errorHasRootCause(error){
    return isErrorSignaturePropertyPresent(error, 'rootCause');
}

function errorHasDate(error){
    return isErrorValuePropertyPresent(error, 'user_crash_date');
}

function isErrorSignaturePropertyPresent(error, propertyName){
    var present = false;
    if(isErrorValuePropertyPresent(error, 'signature')){
        var signature = getErrorValueProperty(error, 'signature');
        if(signature[propertyName]){
            present = true;
        }
    }
    return present;
}

function isErrorValuePropertyPresent(error, propertyName){
    return (error.value[propertyName] ? true : false);
}


