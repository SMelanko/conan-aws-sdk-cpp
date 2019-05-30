from conans import ConanFile, CMake, tools
import os

def merge_dicts_for_sdk(a, b):
    res = a.copy()
    res.update(b)
    return res

class AwssdkcppConan(ConanFile):
    name = "aws-sdk-cpp"
    version = "1.7.113"
    license = "Apache 2.0"
    url = "https://github.com/SMelanko/conan-aws-sdk-cpp"
    description = "Conan Package for aws-sdk-cpp"
    short_paths = True
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"
    requires = "zlib/1.2.11@conan/stable"
    sdks = ("access-management",
            "acm",
            "acm-pca",
            "alexaforbusiness",
            "amplify",
            "apigateway",
            "apigatewaymanagementapi",
            "apigatewayv2",
            "application-autoscaling",
            "appmesh",
            "appstream",
            "appsync",
            "athena",
            "autoscaling",
            "autoscaling-plans",
            "AWSMigrationHub",
            "awstransfer",
            "batch",
            "budgets",
            "ce",
            "chime",
            "cloud9",
            "clouddirectory",
            "cloudformation",
            "cloudfront",
            "cloudfront-integration-tests",
            "cloudhsm",
            "cloudhsmv2",
            "cloudsearch",
            "cloudsearchdomain",
            "cloudtrail",
            "codebuild",
            "codecommit",
            "codedeploy",
            "codepipeline",
            "codestar",
            "cognito-identity",
            "cognitoidentity-integration-tests",
            "cognito-idp",
            "cognito-sync",
            "comprehend",
            "comprehendmedical",
            "config",
            "connect",
            "core",
            "core-tests",
            "cur",
            "custom-service-integration-tests",
            "datapipeline",
            "datasync",
            "dax",
            "devicefarm",
            "directconnect",
            "discovery",
            "dlm",
            "dms",
            "docdb",
            "ds",
            "dynamodb",
            "dynamodb-integration-tests",
            "dynamodbstreams",
            "ec2",
            "ec2-integration-tests",
            "ecr",
            "ecs",
            "eks",
            "elasticache",
            "elasticbeanstalk",
            "elasticfilesystem",
            "elasticloadbalancing",
            "elasticloadbalancingv2",
            "elasticmapreduce",
            "elastictranscoder",
            "email",
            "es",
            "events",
            "firehose",
            "fms",
            "fsx",
            "gamelift",
            "glacier",
            "globalaccelerator",
            "glue",
            "greengrass",
            "guardduty",
            "health",
            "iam",
            "identity-management",
            "identity-management-tests",
            "importexport",
            "inspector",
            "iot",
            "iot1click-devices",
            "iot1click-projects",
            "iotanalytics",
            "iot-data",
            "iot-jobs-data",
            "kafka",
            "kinesis",
            "kinesisanalytics",
            "kinesisanalyticsv2",
            "kinesisvideo",
            "kinesis-video-archived-media",
            "kinesis-video-media",
            "kms",
            "lambda",
            "lambda-integration-tests",
            "lex",
            "lex-models",
            "license-manager",
            "lightsail",
            "logs",
            "machinelearning",
            "macie",
            "marketplacecommerceanalytics",
            "marketplace-entitlement",
            "mediaconnect",
            "mediaconvert",
            "medialive",
            "mediapackage",
            "mediastore",
            "mediastore-data",
            "mediatailor",
            "meteringmarketplace",
            "mobile",
            "mobileanalytics",
            "monitoring",
            "mq",
            "mturk-requester",
            "neptune",
            "opsworks",
            "opsworkscm",
            "organizations",
            "pi",
            "pinpoint",
            "pinpoint-email",
            "polly",
            "polly-sample",
            "pricing",
            "queues",
            "quicksight",
            "ram",
            "rds",
            "rds-data",
            "redshift",
            "redshift-integration-tests",
            "rekognition",
            "resource-groups",
            "resourcegroupstaggingapi",
            "robomaker",
            "route53",
            "route53domains",
            "route53resolver",
            "s3",
            "s3control",
            "s3control-integration-tests",
            "s3-encryption",
            "s3-encryption-integration-tests",
            "s3-encryption-tests",
            "s3-integration-tests",
            "sagemaker",
            "sagemaker-runtime",
            "sdb",
            "secretsmanager",
            "securityhub",
            "serverlessrepo",
            "servicecatalog",
            "servicediscovery",
            "shield",
            "signer",
            "sms",
            "sms-voice",
            "snowball",
            "sns",
            "sqs",
            "sqs-integration-tests",
            "ssm",
            "states",
            "storagegateway",
            "sts",
            "support",
            "swf",
            "text-to-speech",
            "text-to-speech-tests",
            "transcribe",
            "transfer",
            "transfer-tests",
            "translate",
            "waf",
            "waf-regional",
            "workdocs",
            "workmail",
            "workspaces",
            "xray"
           )
    options = merge_dicts_for_sdk({"build_" + x: [True, False] for x in sdks}, {
            "shared": [True, False],
            "min_size": [True, False]
        })
    default_options = ("shared=False","min_size=False") + tuple("build_" + x + "=False" for x in sdks)

    def configure(self):
        if self.settings.os != "Windows":
            if self.settings.os != "Macos":
                self.requires("OpenSSL/1.0.2l@conan/stable")
            self.requires("libcurl/7.56.1@bincrafters/stable")

    def source(self):
        tools.download("https://github.com/aws/aws-sdk-cpp/archive/%s.tar.gz" % self.version, "aws-sdk-cpp.tar.gz")
        tools.unzip("aws-sdk-cpp.tar.gz")
        os.unlink("aws-sdk-cpp.tar.gz")

        # This small hack might be useful to guarantee proper /MT /MD linkage in MSVC
        # if the packaged project doesn't have variables to set it properly
        tools.replace_in_file("aws-sdk-cpp-%s/CMakeLists.txt" % self.version, "project(\"aws-cpp-sdk-all\" VERSION \"${PROJECT_VERSION}\" LANGUAGES CXX)", '''project(aws-cpp-sdk-all VERSION "${PROJECT_VERSION}" LANGUAGES CXX)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        build_only = list([])
        for sdk in self.sdks:
            if getattr(self.options, "build_" + sdk):
                build_only.append(sdk)

        cmake.definitions["BUILD_ONLY"] = ";".join(build_only)
        cmake.definitions["ENABLE_UNITY_BUILD"] = "ON"
        cmake.definitions["ENABLE_TESTING"] = "OFF"
        cmake.definitions["AUTORUN_UNIT_TESTS"] = "OFF"
        cmake.definitions["CUSTOM_MEMORY_MANAGEMENT"] = 0

        cmake.definitions["MINIMIZE_SIZE"] = "ON" if self.options.min_size else "OFF"
        cmake.definitions["BUILD_SHARED_LIBS"] = "ON" if self.options.shared else "OFF"
        cmake.definitions["FORCE_SHARED_CRT"] = "ON" if self.options.shared else "OFF"

        cmake.configure(source_dir="%s/aws-sdk-cpp-%s" % (self.source_folder, self.version))
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        libs = list([])

        if self.settings.os == "Windows":
            libs.append("winhttp")
            libs.append("wininet")
            libs.append("bcrypt")
            libs.append("userenv")
            libs.append("version")
            libs.append("ws2_32")

        for sdk in self.sdks:
            if getattr(self.options, "build_" + sdk):
                libs.append("aws-cpp-sdk-" + sdk)
        libs.append("aws-cpp-sdk-core")

        libs.append("aws-c-common")
        libs.append("aws-c-event-stream")
        libs.append("aws-checksums")

        self.cpp_info.libs = libs
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.includedirs = ["include"]
