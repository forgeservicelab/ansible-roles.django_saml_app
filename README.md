# Sample role installing Django configured with SAML Service Provider

The role will install and configure Django, djangosaml2 and some more things. you will be able to log in via your Identity Provider.

As YAML IdP needs to be aware of SPs that connect to it, you will need to explicitly specify the hostname of the SP in your IdP (at least in the case of SimpleSAMLPHP).

In the case of SimpleSAMLPHP, you need to put following to `metadata/saml20-sp-remote.php`:

```
$metadata['<your_sp_fqdn>/saml2/metadata/'] = array(
        'AssertionConsumerService' => 'http://<your_sp_fqdn>/saml2/acs/',
        'SingleLogoutService' => 'http://<your_sp_fqdn>/saml2/ls/',
);
```

I suppose it will be analogical in other IdP implementations.

## Parameters

The roles can be included as:

```
  - role: django_saml_app
    django_saml_app_idp: https://idp.forgeservicelab.fi
```
Where `django\_saml\_app\_idp` is fqdn of your (hopefully SimpleSAMLPHP) Identity provider.

