import meraki
# #################################################### PARAMETERS ######################################################
organization_id = 'Organization Name'
API_KEY = 'MerakiAPIKey'
password = 'VeryRanD0mPassw0rd1'
# ######################################################################################################################
networks = []


def pull_organization_id():
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizations()
    print(response)
    for dicti in response:
        name = dicti["name"]
        if name == organization_id:
            org_id = dicti["id"]
            print("#################################################")
            print(name + "\n" + "Organization ID: " + org_id)
            print("#################################################")
            return org_id
        else:
            continue


def pull_organization_networks(ident):
    net_dictionary = {}
    dashboard = meraki.DashboardAPI(API_KEY)
    response = dashboard.organizations.getOrganizationNetworks(ident, total_pages='all')
    print(response)
    for network in response:
        name = network['name']
        n_id = network['id']
        # print(name + " : " + n_id)
        net_dictionary[name] = n_id
    print(net_dictionary)
    return net_dictionary


def extract_vpn_account(resp):
    id_list = []
    email_list = []
    name_list = []
    accounttype_list = []
    authorizations_list = []
    for r in resp:
        if r['accountType'] == 'Client VPN':
            id_list.append(r['id'])
            email_list.append(r['email'])
            name_list.append(r['name'])
            accounttype_list.append(r['accountType'])
            authorizations_list.append(r['authorizations'])
    return id_list, email_list, name_list, accounttype_list, authorizations_list


def reset_vpn_password(netid, parameters):
    dashboard = meraki.DashboardAPI(API_KEY)
    clientid = parameters[0]
    emaillist = parameters[1]
    namelist = parameters[2]
    accounttype = parameters[3]
    authorizations = parameters[4]
    # print(clientid)
    for i in range(len(clientid)):
        print('\n' + 'id:' + clientid[i] + '\n' + 'email:' + emaillist[i] + '\n' + 'name:' + namelist[i] + '\n' +
              "acountType:" + accounttype[i] + '\n' + 'password:' + password + '\n' + 'authorization:' +
              str(authorizations[i]) + '\n')

        response = dashboard.networks.updateNetworkMerakiAuthUser(netid, id=clientid[i], email=emaillist[i],
                                                                  name=namelist[i], accountType=accounttype[i],
                                                                  password=password[i],
                                                                  authorizations=authorizations[i])
        print(response)


def pull_and_reset_vpn_users(api, netid):
    network_list = []
    name_list = []
    dashboard = meraki.DashboardAPI(api)
    for n in netid:
        network_list.append(netid[n])
        name_list.append(n)
        # print(network_list)
    for net in range(len(network_list)):
        try:
            response = dashboard.networks.getNetworkMerakiAuthUsers(network_list[net])

            # print(response)
            filename = name_list[net] + "_" + "vpnreset_log.txt"
            saveoutput = open(filename, "a+")
            readoutput = response
            saveoutput.write(str(readoutput))
            accounts = extract_vpn_account(response)
            # print(accounts)
            reset_vpn_password(network_list[net], accounts)
        except:
            print('ERROR')


def reset_password():
    org_id = pull_organization_id()
    net = pull_organization_networks(org_id)
    pull_and_reset_vpn_users(API_KEY, net)


reset_password()
